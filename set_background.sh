#!/bin/bash

BACKGROUND_IMAGE='/opt/netacad-vm-background.jpg'
# For Gnome
gsettings set org.gnome.desktop.background picture-uri '$BACKGROUND_IMAGE'
# For MATE
# gsettings set org.mate.background picture-filename {$BACKGROUND_IMAGE}