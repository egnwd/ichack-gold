#!/bin/bash

FILE_NAME='w.jpg'
POGO_ADDRESS='00-04-48-17-33-7D'
nc -l 0.0.0.0 1234 && \
osascript -e 'tell application "Bluetooth File Exchange"' -e 'send file POSIX path of "w.jpg" to device "00-04-48-17-33-7D"' -e 'end tell' && \
echo "printing" && \
sleep 45 && \
curl -d "id=6&letter=W&idx=1" 129.31.234.152:3000/done && \
echo foo | nc 129.31.234.152 1234
