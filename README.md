# ESPNotifyButton
A ESP8266 based button that sends you a Telegram notification when pressed using MicroPython!

Note: This is just a quick'n'dirty toy example for using MicroPython.

## Build
Since we are using axtls for API calls we need to build micropython with
`-DRT_EXTRA=5120` (was `-DRT_EXTRA=4096`) in file `ports/esp8266/Makefile`!
This is due to the maximum packet size of the underlying TLS communication stream.

## Configuration
Copy `config.json.default` to `config.json` and adjust it to your needs. Once uploaded reset the board to load the updated configuration.

## Hardware
The finished button:

![Finished Button](https://github.com/ngandrass/ESPNotifyButton/raw/master/example/button.jpg)
