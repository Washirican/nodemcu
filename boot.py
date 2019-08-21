import gc
import webrepl

webrepl.start()
gc.collect()

import network
import time
import machine

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

try:
    with open("passwords.txt") as f:
        connections = f.readlines()
except OSError:
    print("No passwords.txt file!")
    connections = []

for connection in connections:
    station, password = connection.split()

    # print("Connecting to {}.".format(station))
    # print('Password: {}'.format(password))

    # sta_if.connect(station, password)
    sta_if.connect('V838 Monocerotis-2G', 'Monkeys2006')

    for i in range(15):
        print(".")

        if sta_if.isconnected():
            break

        time.sleep(1)

    if sta_if.isconnected():
        break
    else:
        print("Connection could not be made.\n")

red_led = machine.Pin(16, machine.Pin.OUT)
# blue_led = machine.Pin(2, machine.Pin.OUT)


def blink(length):
    red_led.value(0)
    # blue_led.value(1)

    time.sleep(length)

    red_led.value(1)
    # blue_led.value(0)


if sta_if.isconnected():
    ip = sta_if.ifconfig()[0].split('.')[3]
    print('IP Address: {}'.format(sta_if.ifconfig()[0]))
    print("Connected as: {}".format(ip))

    for digit in ip:
        blink(.1)
        time.sleep(.1)
        blink(.1)
        time.sleep(2)

        for i in range(int(digit)):
            blink(.5)
            time.sleep(.5)

        time.sleep(2)

# red_led.value(1)
# blue_led.value(1)
