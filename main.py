import os
from pathlib import Path

def main():
    home_dir = Path.home() # Path to user's home directory
    steam_prefixes_dir = home_dir / "SteamPrefixes"
    multiple_paths = False # If there are multiple steam paths, and user wants to use them all
    steam_paths = [] # List of all found steam paths
    steam_path = "" # User's chosen steam path
    

    # Creates directory in user's home folder to put symbolic links
    if not Path.is_dir(steam_prefixes_dir):
        print(f"Creating directory for links to prefixes at {steam_prefixes_dir}")
        Path.mkdir(steam_prefixes_dir)

    # Removing uninstalled games' symlinks
    for link in os.listdir(steam_prefixes_dir):
        path = steam_prefixes_dir / link
        if not os.path.exists(os.readlink(path)):
            print(f"{link} seems to have been uninstalled, deleting symlink")
            os.remove(path)
    

    # Finding Steam paths in user's home directory
    print("Searching for steam install in directory: ", home_dir)
    for root, dirs, files in os.walk(home_dir, topdown=True):
        for d in dirs:
            path = os.path.join(root, d)
            if path.endswith("steamapps/common"):
                print("Found one at: ", path)
                steam_paths.append(path)

    # Handling multiple steam installations
    if len(steam_paths) > 1:
        ask_again = True
        user_input = ""
        count = 1
        while ask_again:
            print("More than one steam path has been found, please select one")
            count = 1
            for path in steam_paths:
                print(f"  - {path} ({count})")
                count += 1
            user_input = input("Please select your steam installation (Choose 0 if you're unsure or use all of them): ")
            if not user_input.isdigit():
                print("Please select a valid number")  
            elif int(user_input) < 0 or int(user_input) > count:
                print("Please select a number within the range")
            else:
                ask_again = False
        user_input = int(user_input)
        if user_input != 0:
            steam_paths = [steam_paths[user_input - 1]]

    # Linking game name and appID
    print("Getting appids and names of installed games, and creating symlinks")
    for path in steam_paths:
        path = Path(path).parent
        compat_path = path / "compatdata"
        for game in path.glob("./appmanifest_*.acf"):
            appid = ""
            gamename = ""
            # Reads all appmanifest files to get appid and app name
            if Path.is_file(game):
                with open(game, 'r') as f:
                    for line in f.readlines():
                        if '"appid"' in line:
                            parts = line.split('"')
                            appid = parts[3]
                        if '"name"' in line:
                            parts = line.split('"')
                            gamename = parts[3]
            print(f"--------------\nFound: {gamename} -- {appid}")
            # Creates symlinks to steam_prefixes_dir
            app_compat_path = compat_path / appid
            dest_path = steam_prefixes_dir / gamename
            if Path.is_dir(app_compat_path):
                if not Path.is_dir(dest_path):
                    print(f"Creating symlink for: {gamename}")
                    os.symlink(app_compat_path, dest_path, target_is_directory=True)
                else:
                    print("Symlink already exists")
            else:
                print(f"{gamename} does not have a prefix")



if __name__ == "__main__":
    main()
