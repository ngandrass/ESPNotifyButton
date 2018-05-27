# ESPNotifyButton
A ESP8266 based button that sends you a notification when pressed using MicroPython!

## Build
Since we are using axtls for API calls we need to build micropython with
`-DRT_EXTRA=5120` (was `-DRT_EXTRA=4096`) in file `ports/esp8266/Makefile`!
This is due to the maximum packet size of the underlying TLS communication stream.