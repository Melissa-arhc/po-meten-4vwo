from microbit import *
import radio

# Initialiseer de radiomodule
radio.on()
radio.config(group=23)

SENSOR_ID = "U00001"
SENSOR_PWD = "123456"
SENSOR_NAME = "t"


while True:
    if button_a.was_pressed():
        # haal temparatuur op van microbit
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
