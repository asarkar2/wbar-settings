#!/bin/bash

install_direc='/usr/local/share/wbar-settings'
script_direc='/usr/local/bin'
icon_direc='/usr/local/share/pixmaps'
desktop_direc='/usr/local/share/applications'

sudo rm -rf "${install_direc}"
sudo rm "${script_direc}"/wbar-settings
sudo rm "${icon_direc}"/wbar.png
sudo rm "${desktop_direc}"/wbar-settings.desktop
