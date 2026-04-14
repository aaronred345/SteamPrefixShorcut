#! /usr/bin/env python
"""
SteamPrefixShortcut

This tool creates easy-to-find symbolic links to Proton/Wine prefixes for Steam games.
It automatically locates Steam installations, identifies games, and creates symbolic links
named after each game in a dedicated directory (~/SteamPrefixes).

Author: Aaron J Gerbert
License: MIT
"""

import os
import re
from pathlib import Path

def main():
    """
    Main function that performs the following operations:
    1. Creates a directory for symbolic links if it doesn't exist
    2. Cleans up symlinks for uninstalled games
    3. Locates Steam installations in the user's home directory
    4. Handles multiple Steam installations if found
    5. Creates symbolic links from game names to their prefixes
    """
    home_dir = Path.home()  # Path to user's home directory
    steam_prefixes_dir = home_dir / "SteamPrefixes"
    multiple_paths = False  # If there are multiple steam paths, and user wants to use them all
    steam_paths = []  # List of all found steam paths
    steam_path = ""  # User's chosen steam path
    
    # SECTION 1: DIRECTORY SETUP
    # Creates a dedicated directory in the user's home folder to store symbolic links to game prefixes
    # This directory serves as a central, easy-to-access location for all game prefixes
    # The directory is created only if it doesn't already exist to avoid errors
    if not Path.is_dir(steam_prefixes_dir):
        print(f"Creating directory for links to prefixes at {steam_prefixes_dir}")
        Path.mkdir(steam_prefixes_dir)

    # SECTION 2: CLEANUP OF OUTDATED SYMLINKS
    # Checks each symbolic link in the SteamPrefixes directory to ensure it points to a valid location
    # If a game has been uninstalled, its prefix directory will no longer exist
    # This loop identifies broken symlinks (pointing to non-existent locations) and removes them
    # This ensures the SteamPrefixes directory stays up-to-date with currently installed games only
    for link in os.listdir(steam_prefixes_dir):
        path = steam_prefixes_dir / link
        if not os.path.exists(os.readlink(path)):
            print(f"{link} seems to have been uninstalled, deleting symlink")
            os.remove(path)
    
    # SECTION 3: STEAM INSTALLATION DETECTION
    # This section uses two different methods to locate Steam installations in the user's home directory
    # Method 1: Looks for the standard .steam/root directory (common on many Linux distributions)
    # Method 2: Recursively searches through the home directory for paths ending with steamapps/common
    # Both methods read the libraryfolders.vdf file to find all configured Steam library locations
    # This handles cases where users have multiple Steam libraries across different drives/locations
    print("Searching for steam install")
    if (Path.is_dir(home_dir / ".steam/root")):
        # First method: Check standard .steam/root directory
        # Code here courtesy of JonathanY234 (modified version of this in the next else block)
        with open(home_dir / ".steam/root/steamapps/libraryfolders.vdf", "r") as f:
            content = f.read()
        # Extract all Steam library paths from the VDF file using regex pattern matching
        # The pattern looks for "path" "VALUE" pairs in the VDF file format
        steam_paths = re.findall(r'\s*"path"\s+"([^"]+)"', content)
        # Convert each path to include the steamapps/common subdirectory where games are installed
        steam_paths = [os.path.join(path, "steamapps/common") for path in steam_paths]
        print(steam_paths)
    else:
        # Second method: Search through home directory for steamapps/common paths
        # This is a fallback method that recursively walks through the home directory
        # It's more thorough but potentially slower than the first method
        for root, dirs, files in os.walk(home_dir, topdown=True):
            for d in dirs:
                path = os.path.join(root, d)
                if path.endswith("steamapps/common"):
                    path = Path(path)
                    # Read the libraryfolders.vdf file to find all configured Steam libraries
                    # This file contains information about all Steam library locations
                    with open(path.parent / "libraryfolders.vdf") as f:
                        content = f.read()
                    # Extract paths using the same regex pattern as in method 1
                    paths = re.findall(r'\s*"path"\s+"([^"]+)"', content)
                    # Add each path to the steam_paths list if not already present
                    for p in paths:
                        if Path(p) / "steaamapps/common" not in steam_paths:
                            steam_paths.append(Path(p) / "steamapps/common")

    # SECTION 4: MULTIPLE STEAM LIBRARY HANDLING
    # This section handles the case where multiple Steam library locations are detected
    # It provides an interactive prompt for the user to select which library to use
    # The user can select a specific library by number, or select 0 to use all libraries
    # This is important for users with games installed across multiple drives or locations
    if len(steam_paths) > 1:
        ask_again = True
        user_input = ""
        count = 1
        # Interactive selection loop that continues until a valid selection is made
        # Shows a numbered list of all detected Steam library paths
        while ask_again:
            print("More than one steam path has been found, please select one")
            count = 1
            for path in steam_paths:
                print(f"  - {path} ({count})")
                count += 1
            user_input = input("Please select your steam installation (Choose 0 if you're unsure or use all of them): ")
            # Input validation to ensure the selection is a valid number within range
            if not user_input.isdigit():
                print("Please select a valid number")  
            elif int(user_input) < 0 or int(user_input) > count:
                print("Please select a number within the range")
            else:
                ask_again = False
        user_input = int(user_input)
        # If user selects a specific path, filter the list to only that path
        # If user selects 0, keep all paths (use all of them)
        # This allows flexibility in handling multiple libraries based on user preference
        if user_input != 0:
            steam_paths = [steam_paths[user_input - 1]]

    # SECTION 5: SYMLINK CREATION FOR GAME PREFIXES
    # This section is the core functionality of the tool. For each Steam library path:
    # 1. It navigates to the parent directory (from 'steamapps/common' to just 'steamapps')
    # 2. It identifies the 'compatdata' directory where Proton/Wine prefixes are stored
    # 3. It reads all appmanifest_*.acf files to extract game names and their AppIDs
    # 4. It creates symbolic links from ~/SteamPrefixes/[Game Name] to the actual prefix location
    print("Getting appids and names of installed games, and creating symlinks")
    for path in steam_paths:
        # Move up one directory level from steamapps/common to just steamapps
        path = Path(path).parent
        # The compatdata directory contains all the Proton/Wine prefixes, organized by AppID
        compat_path = path / "compatdata"
        # Process each application manifest file to extract game info
        # Steam stores game metadata in appmanifest_[AppID].acf files
        for game in path.glob("./appmanifest_*.acf"):
            appid = ""
            gamename = ""
            # Reads each appmanifest file line by line to extract the AppID and game name
            # These files use a custom Valve format (VDF) that we parse with simple string operations
            if Path.is_file(game):
                with open(game, 'r') as f:
                    for line in f.readlines():
                        # Extract the AppID from the manifest (unique identifier for each game)
                        # This is used to locate the game's prefix directory
                        if '"appid"' in line:
                            parts = line.split('"')
                            appid = parts[3]
                        # Extract the game name from the manifest
                        # This will be used as the symlink name for easy identification
                        if '"name"' in line:
                            parts = line.split('"')
                            gamename = parts[3]
            print(f"--------------\nFound: {gamename} -- {appid}")
            
            # Creates symlinks from game names to their actual prefix directories
            # The source is the actual prefix directory: [Steam Library]/steamapps/compatdata/[AppID]
            # The destination is the user-friendly named link: ~/SteamPrefixes/[Game Name]
            app_compat_path = compat_path / appid
            dest_path = steam_prefixes_dir / gamename.replace("/", "-")
            if Path.is_dir(app_compat_path):
                # Create symlink if it doesn't already exist (avoids errors on repeated runs)
                # Some games might not have prefixes if they don't use Proton/Wine
                if not Path.is_dir(dest_path):
                    print(f"Creating symlink for: {gamename}")
                    os.symlink(app_compat_path, dest_path, target_is_directory=True)
                else:
                    print("Symlink already exists")
            else:
                # This happens for games that don't use Proton/Wine (e.g., native Linux games)
                # or for games that haven't been run yet since installation
                print(f"{gamename} does not have a prefix")


if __name__ == "__main__":
    main()