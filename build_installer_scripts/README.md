# Build Installer Scripts

This directory contains scripts to build standalone installer executables for the Project Management software setup script (`cross_platform_setup.py`) for Linux, Windows, and macOS.

## Prerequisites

- Python 3.x installed
- PyInstaller installed (`pip install pyinstaller`)
- Access to build environments for each target platform (Linux, Windows, macOS)

## Usage

Run the build script to generate standalone executables:

```bash
bash build_installers.sh
```

The built executables will be placed in the `dist_installers` directory.

## Notes

- The Windows executable is built with the `--windowed` option to suppress the console window.
- You need to run the build script on each target platform or use cross-compilation tools.
- The generated executables include all dependencies and can be distributed to users without requiring Python installation.

## After Building

Distribute the appropriate executable file to your users based on their operating system. Users can run the executable to start the installation process with GUI prompts and dependency checks.
