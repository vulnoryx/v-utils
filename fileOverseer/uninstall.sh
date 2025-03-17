#!/bin/bash

serviceFileDest="/etc/systemd/system/"
pythonInstallDir="/home/$USER/scripts/"

echo "Uninstalling fileOverseer..."

# stopping service
sudo systemctl stop fileOverseer.service
sudo systemctl disable fileOverseer.service

# removing files
sudo rm -f $serviceFileDest/fileOverseer.service
sudo rm -f $pythonInstallDir/fileOverseer.py

echo "Done"