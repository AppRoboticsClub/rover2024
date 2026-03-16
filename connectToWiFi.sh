#!/bin/bash

CURR_CONN="$(nmcli -t -f NAME con show --active)"
if [[ -n CURR_CONN ]]
then
  sudo nmcli con down $CURR_CONN >/dev/null 2>/dev/null
  echo "Disconnected from hotspot first."
fi
echo "Connecting to APPSTATE-GUEST, this may take a moment."
sudo nmcli con delete APPSTATE-GUEST >/dev/null 2>/dev/null  # redirect stderr to null
sleep 2
sudo nmcli device wifi connect "APPSTATE-GUEST" >/dev/null 2>/dev/null &
wait "$!" || true
if [[ "$(sudo nmcli -f NAME con show --active)" != "APPSTATE-GUEST" ]]
then
  echo "Connection failed! Please try again."
fi
