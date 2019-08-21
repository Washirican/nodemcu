import time

from machine import Pin


led = Pin(2, Pin.OUT)
led2 = Pin(16, Pin.OUT)

for i in range(5):
    time.sleep(.5)
    led.value(1)
    led2.value(0)

    time.sleep(.5)
    led.value(0)
    led2.value(1)
led.value(1)
led2.value(1)
