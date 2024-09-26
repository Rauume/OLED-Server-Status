#!/bin/bash

DEVICE="/dev/serial/by-id/usb-MicroPython_Board_in_FS_mode_e6614103e72b1c37-if00"
NET_INTERFACE="ens18"

if [ ! -e "${DEVICE}" ]; then
  echo "no \"${DEVICE}\" device found"
  exit 1
fi

stty -F "${DEVICE}" 115200 clocal -hup

ip=$(ifconfig "${NET_INTERFACE}" | grep "inet " | tr -s ' ' '\t' | cut -f 3)
date=$(date +"%H:%M")
cpu=$(mpstat 1 1 | awk '/^Average/ {print 100 - $12 " %"}')
temp=$(cat /sys/class/thermal/thermal_zone0/temp)


#The space before EOF is important, so the microcontroller recognises the end of data being sent.
cat > "${DEVICE}" << EOF
   date: ${date}
     ip: ${ip}
    cpu: ${cpu}
cpu deg: $(($temp / 1000))c

EOF