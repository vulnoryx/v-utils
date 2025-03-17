#!/bin/bash

# configure service file
echo "=[ File Overseer install setup ]="
read -p 'Directory to monitor (leave empty for /home/$USER/Downloads): ' monitorPath
read -p "Script install directory (leave empty for /home/$USER/scripts/): " installLocation

serviceFileDest="/etc/systemd/system/"
pythonInstallDir="/home/$USER/scripts/"

if [ "$monitorPath" == "" ]
then
    monitorPath="/home/$USER/Downloads/"
fi

if [ "$installLocation" != "" ]
then
    if [[ "${installLocation: -1}" != "/" ]]
    then
        installLocation=$installLocation"/"
    fi

    pythonInstallDir=$installLocation
fi

echo "----------"
echo "Monitor path: $monitorPath"
echo "Install path: $pythonInstallDir"
echo "FileOverseer.service file will be installed in $serviceFileDest"
read -p "Is the information correct? (Y/n): " infoCorrect

if [ "$infoCorrect" == "n" ] || [ "$infoCorrect" == "N" ] || [ "$infoCorrect" == "no" ] || [ "$infoCorrect" == "No" ]
then
    echo "Exiting..."
    exit 0
else
    echo "Proceeding with installation..."
fi

# create service file
cat > fileOverseer.service <<EOF
[Unit]
Description=File Overseer
[Service]
Type=simple
User=$USER
ExecStart=/usr/bin/python3 ${pythonInstallDir}fileOverseer.py $monitorPath

[Install]
WantedBy=multi-user.target
EOF

regularUser=$USER

# actually install
sudo rm -f $serviceFileDest/fileOverseer.service
sudo rm -f $pythonInstallDir/fileOverseer.py

sudo cp ./fileOverseer.service $serviceFileDest
sudo cp ./fileOverseer.py $pythonInstallDir

sudo chown $regularUser:$regularUser $pythonInstallDir/fileOverseer.py

echo "Starting services..."

# start service
sudo systemctl enable fileOverseer.service
sudo systemctl start fileOverseer.service

echo "Installation complete"