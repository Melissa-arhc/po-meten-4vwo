from microbit import *
import radio

# Initialiseer de radiomodule
radio.on()
radio.config(group=23)

SENSOR_ID = "191896"
SENSOR_PWD = "TOP_SECRET"
SENSOR_NAME = "temp"


while True:
    if button_a.was_pressed():
        # krijg temparatuur van microbit
        value = temperature()
        display.show(value)
        payload = "id={},p={},n={},v={}".format(
            SENSOR_ID, SENSOR_PWD, SENSOR_NAME, value
        )
        print(payload)
        # stuur de tekst via de radio
        radio.send(payload)

        # wachten
        sleep(1000)

        # wissen
        display.clear()
