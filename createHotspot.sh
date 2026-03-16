#!/bin/bash

sudo nmcli con add con-name hotspot ifname wlan0 type wifi ssid "Rover"
sudo nmcli con modify hotspot wifi-sec.key-mgmt wpa-psk
sudo nmcli con modify hotspot wifi-sec.psk "rover12345"
sudo nmcli con modify hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
sudo nmcli con up hotspot

