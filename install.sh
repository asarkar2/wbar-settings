#!/bin/bash

install_direc='/usr/local/share/wbar-settings'
script_direc='/usr/local/bin'
icon_direc='/usr/local/share/pixmaps'
desktop_direc='/usr/local/share/applications'

# Install script and local icons
sudo mkdir -p "${install_direc}"
sudo cp filedialogpreview.py "${install_direc}"
sudo cp wbar-settings.py "${install_direc}"
sudo cp -R icons/ "${install_direc}"
sudo chmod 755 "${install_direc}"/*.py

# Create link to bin directory
sudo mkdir -p "${script_direc}"
sudo rm -f "${script_direc}"/wbar-settings
sudo ln -s "${install_direc}"/wbar-settings.py ${script_direc}/wbar-settings

# Install icons
sudo mkdir -p "${icon_direc}"
sudo cp icons/wbar.png "${icon_direc}"

# Install desktop file
sudo mkdir -p "${desktop_direc}"
sudo cp wbar-settings.desktop "${desktop_direc}"

