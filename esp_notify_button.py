#!/usr/bin/env python

"""
A ESP8266 based button that sends you a notification when pressed using MicroPython!
"""

__author__ = "Niels Gandraß"
__email__ = "ngandrass@squacu.de"
__version__ = "0.0.1"
__license__ = "MIT"

from machine import Pin, Timer
from urequests import urequests as requests

# Pin mapping
PIN_LED_ONBOARD = Pin(2, mode=Pin.OUT, value=True)
PIN_LED_GREEN   = Pin(5, mode=Pin.OUT, value=False)
PIN_LED_RED     = Pin(4, mode=Pin.OUT, value=False)
PIN_BUTTON      = Pin(12, mode=Pin.IN, pull=Pin.PULL_UP)

CONFIG = {}  # Holds configuration once load_config() was called

BTN_DEADTIM = Timer(-1)  # Timer used for button dead time delay
BTN_DISABLE = False      # If button is in dead time mode


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
        set_led('red')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass

    set_led('green')
    print('Connected to wifi network: ', wlan.ifconfig())


def set_led(state):
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


def send_telegram_msg(text=None, bot_token=None, chat_id=None) -> bool:
    """
    Sends a new telegram message

    :param text: Message text to send. Defaults to CONFIG['telegram']['default_msg']
    :param bot_token: API-token of the bot to use. Defaults to CONFIG['telegram']['bot_token']
    :param chat_id: Chat-ID to send the message to. Defaults to CONFIG['telegram']['chat_id']
    :return: bool indicating if message was send successful
    """
    # Apply defaults if necessary
    if text is None:
        text = CONFIG['telegram']['default_msg']

    if bot_token is None:
        bot_token = CONFIG['telegram']['bot_token']

    if chat_id is None:
        chat_id = CONFIG['telegram']['chat_id']

    # Do API call
    r = requests.get('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(
        bot_token,
        chat_id,
        text
    ))

    # Check if call was successful
    if r.status_code != 200 or not r.json()['ok']:
        return False

    return True


def arm_button(timer=None) -> None:
    """
    (Re-)Enables the trigger button

    :return: None
    """
    global BTN_DISABLE

    set_led('green')
    BTN_DISABLE = False
    print('Armed trigger button')


def button_irqhandler(pin) -> None:
    """
    Interrupt request handler for trigger button interrupt.

    :return: None
    """
    # Ignore button IRQ until re-enabled by timer after dead time
    global BTN_DISABLE

    if BTN_DISABLE:
        return
    else:
        BTN_DISABLE = True

    # Try to send a telegram message
    set_led('orange')

    if not send_telegram_msg():
        set_led('red')

    # Arm timer to re-enable button irq after dead time
    BTN_DEADTIM.init(period=CONFIG['button_deadtime_ms'], mode=Timer.ONE_SHOT, callback=arm_button)


def main() -> None:
    """
    Main entry point. Configures chip, connects to wifi and arms interrupts.

    :return: None
    """
    global CONFIG
    CONFIG = load_config()

    # Connect to wifi
    setup_wifi(CONFIG['wifi_ssid'], CONFIG['wifi_pass'])

    # Configure and arm trigger button
    PIN_BUTTON.irq(handler=button_irqhandler, trigger=Pin.IRQ_FALLING)
    arm_button()


if __name__ == "__main__":
    main()
