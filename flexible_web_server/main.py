try:
    import usocket as socket
except:
    import socket

response_404 = """HTTP/1.0 404 NOT FOUND

<h1>404 Not Found</h1>
"""

response_500 = """HTTP/1.0 500 INTERNAL SERVER ERROR

<h1>500 Internal Server Error</h1>
"""

response_template = """HTTP/1.0 200 OK

%s
"""

import machine
import ntptime, utime
from machine import RTC
from time import sleep

rtc = RTC()
try:
    seconds = ntptime.time()
except:
    seconds = 0
rtc.datetime(utime.localtime(seconds))


led_pin = machine.Pin(9, machine.Pin.OUT)
switch_pin = machine.Pin(10, machine.Pin.IN)
adc = machine.ADC(0)
pwm = machine.Pin(13)
pwm = machine.PWM(pwm)
pwm.duty(1000)


def time():
    body = """<html>
<body>
<h1>Current Time</h1>
<p>%s</p>
</body>
</html>
""" % str(rtc.datetime())

    return response_template % body


def dummy():
    body = "This is a dummy endpoint"
    return response_template % body


def light_on():
    led_pin.value(1)
    body = "You turned a light on!"
    return response_template % body


def light_off():
    led_pin.value(0)
    body = "You turned a light off!"
    return response_template % body


def switch():
    body = "{state: " + str(switch_pin.value()) + "}"
    return response_template % body


def light():
    body = "{value: " + str(adc.read()) + "}"
    return response_template % body


def pwm1000():
    pwm.duty(1000)
    body = "You turned a PWM to 1000 Hz!"
    return response_template % body


def pwm500():
    pwm.duty(500)
    body = "You turned a PWM to 500 Hz!"
    return response_template % body


def pwm250():
    pwm.duty(250)
    body = "You turned a PWM to 250 Hz!"
    return response_template % body


def pwm75():
    pwm.duty(75)
    body = "You turned a PWM to 75 Hz!"
    return response_template % body


def pwm10():
    pwm.duty(10)
    body = "You turned a PWM to 10 Hz!"
    return response_template % body


def home():
    body = """<html>
    <body>
    <h1>NodeMCU Menu</h1>
    <p></p>
    <a href='time'>Current Time</a><br>
    <a href='light_on'>LED On</a><br>
    <a href='light_off'>LED Off</a><br>
    <a href='switch'>Switch State</a><br>
    <a href='light'>Photoresistor State</a><br>
    <a href='pwm1000'>PWM 1000 Hz</a><br>
    <a href='pwm500'>PWM 500 Hz</a><br>
    <a href='pwm250'>PWM 250 Hz</a><br>
    <a href='pwm75'>PWM 75 Hz</a><br>
    <a href='pwm10'>PWM 10 Hz</a><br>
    </body>
    </html>
    """

    # body = '<a href="Current Time">Time</a>'
    return response_template % body


handlers = {
    'time': time,
    'dummy': dummy,
    'light_on': light_on,
    'light_off': light_off,
    'switch': switch,
    'light': light,
    'pwm1000': pwm1000,
    'pwm500': pwm500,
    'pwm250': pwm250,
    'pwm75': pwm75,
    'pwm10': pwm10,
    'home': home,
    }


def main():
    s = socket.socket()
    ai = socket.getaddrinfo("0.0.0.0", 8080)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080")

    while True:
        sleep(1)
        res = s.accept()
        client_s = res[0]
        client_addr = res[1]
        req = client_s.recv(4096)
        print("Request:")
        print(req)

        try:
            path = req.decode().split("\r\n")[0].split(" ")[1]
            handler = handlers[path.strip('/').split('/')[0]]
            response = handler()
        except KeyError:
            response = response_404
        except Exception as e:
            response = response_500
            print(str(e))

        client_s.send(
            b"\r\n".join([line.encode() for line in response.split("\n")]))

        client_s.close()
        print()


main()
