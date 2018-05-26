#!/usr/bin/env python

"""
A ESP8266 based button that sends you a notification when pressed using MicroPython!
"""

__author__ = "Niels Gandraß"
__email__ = "ngandrass@squacu.de"
__version__ = "0.0.1"
__license__ = "MIT"

from machine import Pin

# Pin mapping
PIN_LED_ONBOARD = Pin(2, mode=Pin.OUT, value=True)
PIN_LED_GREEN   = Pin(5, mode=Pin.OUT, value=False)
PIN_LED_RED     = Pin(4, mode=Pin.OUT, value=False)
PIN_BUTTON      = Pin(12, mode=Pin.IN, pull=Pin.PULL_UP)

CONFIG = {}  # Holds configuration once load_config() was called


def load_config(cfg_file="config.json") -> dict:
    """
    Loads the configuration from the given cfg_file.

    :param cfg_file: Config file containing the configuration JSON.
    :return: dict containing config parameters
    """
    with open(cfg_file, 'r') as json_file:
        import ujson
        return ujson.loads(json_file.read())


def setup_wifi(ssid, password) -> None:
    """
    Configures the wifi connection.

    :param ssid: SSID of the network to connect to.
    :param password: Password of the network to connect to.
    :return: None
    """
    import network
    network.WLAN(network.AP_IF).active(False)

    # TODO: Determine micropython behaviour on wifi disconnect
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to wifi network "', ssid, '"...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass

    print('Connected to wifi network: ', wlan.ifconfig())


def setLed(state):
    """
    Updates the state of the LED.

    :param state: The desired color ('green', 'orange', 'red) or 'off.
    :return: None
    """
    if state == 'green':
        PIN_LED_GREEN.on()
        PIN_LED_RED.off()
    elif state == 'orange':
        PIN_LED_GREEN.on()
        PIN_LED_RED.on()
    elif state == 'red':
        PIN_LED_GREEN.off()
        PIN_LED_RED.on()
    else:
        PIN_LED_GREEN.off()
        PIN_LED_RED.off()


def main():
    global CONFIG
    CONFIG = load_config()

    setLed('red')
    setup_wifi(CONFIG['wifi_ssid'], CONFIG['wifi_pass'])
    setLed('orange')


if __name__ == "__main__":
    main()
