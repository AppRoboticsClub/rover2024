#!/bin/bash

read -t 10 -p "Type something within 10 seconds to cancel startup" userInput
if [ -z "$userInput" ]; then
	echo "Starting rover"
	bash ~/startrover.sh
fi


#start wifi
#touch /home/appbot/Desktop/sdhfjfhsdjkfkjlsdsjkf.txt
#echo $DISPLAY >> /home/appbot/Desktop/dis.txt
#sleep 1m
#x-terminal-emulator -e "bash /home/appbot/Desktop/appRobo/startup.sh"
