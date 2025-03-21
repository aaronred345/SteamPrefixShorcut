# SteamPrefixShortcut

A Linux utility that creates easy-to-find symbolic links to Proton/Wine prefixes for installed Steam games.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Uninstallation](#uninstallation)
6. [How It Works](#how-it-works)
7. [Usage](#usage)
8. [File Structure](#file-structure)
9. [Technical Details](#technical-details)
10. [Troubleshooting](#troubleshooting)
11. [License](#license)

## Overview

SteamPrefixShortcut is a Linux utility that creates easy-to-find symbolic links to Proton/Wine prefixes for installed Steam games. The tool automatically searches for Steam installations in your home directory, identifies installed games, and creates symbolic links named after each game in a dedicated directory (`~/SteamPrefixes`).

This utility is particularly useful for Linux gamers who need to access or modify their game prefixes, as it provides a centralized, clearly labeled location for all game prefixes rather than navigating through Steam's nested directory structure.

## Features

- **Automatic Steam Installation Detection**: Finds Steam installations in the user's home directory
- **Multiple Steam Library Support**: Can handle multiple Steam library locations
- **Intelligent Prefix Management**: Creates symbolic links named after games for easy identification
- **Automatic Cleanup**: Removes links to uninstalled games
- **Startup Integration**: Can run automatically at system login
- **Flexible Installation Options**: Supports both local (user-specific) and global (system-wide) installation

## Requirements

- Python 3
- GCC or another C compiler (only needed for installation scripts)
- Linux operating system
- Steam installed with Proton-compatible games

## Installation

### Preparing for Installation

Make all scripts executable:
```bash
chmod +x *.sh
```

### Local Installation (User-Specific)

This method installs the tool for the current user only and doesn't require sudo privileges:

```bash
./install-local.sh
```

The local installation:
- Compiles the Python script to a binary using Nuitka
- Installs the binary to `~/.local/bin/steam-prefix`
- Adds a startup entry to your `~/.profile` to run on login
- Cleans up temporary build files

### Global Installation (System-Wide)

This method installs the tool for all users and requires sudo privileges:

```bash
./install-global.sh
```

The global installation:
- Compiles the Python script to a binary using Nuitka
- Installs the binary to `/bin/steam-prefix`
- Creates a startup script in `/etc/profile.d/` to run on system login
- Cleans up temporary build files

## Uninstallation

### Local Uninstallation

If you installed using the local method:

```bash
./uninstall-local.sh
```

This will:
- Remove the binary from `~/.local/bin/steam-prefix`
- Remove the startup entry from `~/.profile`

### Global Uninstallation

If you installed using the global method:

```bash
./uninstall-global.sh
```

This will:
- Remove the binary from `/bin/steam-prefix`
- Remove the startup script from `/etc/profile.d/steam-prefix.sh`

## How It Works

SteamPrefixShortcut performs the following operations:

1. **Directory Setup**: Creates a `~/SteamPrefixes` directory if it doesn't exist
2. **Cleanup**: Removes symlinks to prefixes of uninstalled games
3. **Steam Detection**: Searches for Steam installations in the user's home directory
4. **Library Selection**: If multiple Steam libraries are found, asks the user which to use (or all)
5. **Game Identification**: Reads Steam's application manifest files to get game names and IDs
6. **Symlink Creation**: Creates symbolic links from `~/SteamPrefixes/[Game Name]` to the actual prefix location

## Usage

### Running Manually

If installed:
```bash
steam-prefix
```

If not installed:
```bash
python3 main.py
```

### Automatic Execution

The tool will run automatically at login if installed using either installation method.

### Accessing Game Prefixes

After running the tool, you can access any game's prefix by navigating to:
```bash
cd ~/SteamPrefixes/[Game Name]
```

For example:
```bash
cd ~/SteamPrefixes/Half-Life\ 2
```

## File Structure

- **main.py**: Main Python script that implements the tool's functionality
- **install-local.sh**: Script for local (user-specific) installation
- **install-global.sh**: Script for global (system-wide) installation
- **uninstall-local.sh**: Script to remove local installation
- **uninstall-global.sh**: Script to remove global installation
- **compile.sh**: Helper script to compile the Python script to a binary using Nuitka
- **cleanup.sh**: Helper script to remove temporary build files
- **LICENSE**: MIT license file
- **README.md**: Brief project overview and installation instructions

## Technical Details

### Prefix Location

Steam stores Proton/Wine prefixes in the `compatdata` directory within each Steam library. Each prefix is in a subdirectory named with the game's AppID. This tool creates symbolic links from `~/SteamPrefixes/[Game Name]` to the actual prefix location at `[Steam Library]/steamapps/compatdata/[AppID]`.

### Steam Library Detection

The tool uses two methods to find Steam libraries:
1. First, it checks for the standard `.steam/root` directory in the user's home
2. If that's not found, it walks through the home directory looking for paths ending in `steamapps/common`

For both methods, it reads the `libraryfolders.vdf` file to discover all configured Steam library locations.

### Game Information Extraction

The tool reads `appmanifest_*.acf` files in each Steam library's `steamapps` directory to extract game names and AppIDs.

### Compilation Process

The installation scripts use Nuitka to compile the Python script to a binary. This:
- Creates a standalone executable without Python dependencies
- Improves startup performance
- Allows for easier distribution

## Troubleshooting

### Symlinks Not Created

- Ensure Steam is properly installed and you have at least one game with a Proton/Wine prefix
- Check if the `~/SteamPrefixes` directory exists and you have write permissions
- Run the tool manually to see any error messages

### Multiple Steam Libraries Not Detected

- Make sure all Steam libraries are properly configured in Steam
- The tool only detects libraries in your home directory by default
- Try running the tool manually to select specific libraries

### Tool Not Running at Login

- Check if the binary exists at the expected location (`~/.local/bin/steam-prefix` or `/bin/steam-prefix`)
- Verify that the startup entry was added correctly to `~/.profile` or `/etc/profile.d/`
- Try running the tool manually to check for errors

## License

SteamPrefixShortcut is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Copyright (c) 2024 Aaron J Gerbert