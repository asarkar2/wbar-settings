# wbar-settings
GUI configuration application for wbar dock

## Foreword:

This work was inspired by wbar-config. However, since it is no longer
available on my current linux distribution, I decided to rebuilt it from
scratch. Plus, it was fun.

## License:

The work wbar-settings.py and its associated files (except the icons)
are protected by the GPLv3 license or any later version. The icons are
all from open source and as such carry their respective licenses.

## Requirements:

Install the python3 qt package via apt.
```
sudo apt install python3-pyqt5
```
Alternatively, install it via pip
```
pip3 install pyqt5
```

## Install and uninstall:

Make the `install.sh` and `uninstall.sh` files executable and run them to 
install and/or uninstall the script wbar-settings.py.
```
chmod +x install.sh uninstall.sh
./install.sh # To install
./uninstall.sh # To uninstall
```

## Usage:

After installation the script can be used as follows:
```
wbar-settings
```
in which case it uses the ~/.wbar file if present. Alternatively, to use 
another config file, use the command
```
wbar-settings -c path/to/wbarconfig
```
