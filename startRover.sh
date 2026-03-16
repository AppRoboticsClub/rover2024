#!/bin/bash

cd ~/rover

MAX=5
for ((i=1; i<=MAX; i++))
do
  echo "Attempt $i/$MAX connecting to APPSTATE-GUEST"
  ../connectToWiFi.sh >/dev/null 2>/dev/null &
  wait "$!" || true
  if [[ "$(nmcli -t -f ACTIVE,NAME con show --active)" == "yes:APPSTATE-GUEST" ]]
  then
    break
  fi
done

if (( i > MAX ))
then
  echo "Timed out connecting to APPSTATE-GUEST, won't pull from GitHub!"
else
  echo "Successfully connected to APPSTATE-GUEST! Pulling from GitHub."
  git pull --ff-only

  sudo nmcli con down APPSTATE-GUEST
fi

echo "Starting hotspot! Connect to 'Rover' WiFi with password 'rover12345'"
sudo nmcli con up hotspot

source ~/rover/.venv/bin/activate
echo "Starting Flask webapp! Connect to 10.42.0.1:5001"  # TODO: Make the ip dynamically generated
python ~/rover/main.py
