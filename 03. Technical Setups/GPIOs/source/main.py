# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import *
import time

# LED-Pins wie im Sketch definiert
FIRST_PIN = 8
LAST_PIN  = 13
LED_COUNT = LAST_PIN - FIRST_PIN + 1

# Status jeder LED
led_states = [False] * LED_COUNT

def loop():
    global led_states
    time.sleep(1)  # 1s Delay

    for i in range(LED_COUNT):
        # LED Status toggeln
        led_states[i] = not led_states[i]

        # Status an Zephyr-Sketch senden: Pin-Nummer + Status
        Bridge.call("set_led_state", FIRST_PIN + i, led_states[i])

App.run(user_loop=loop)


