import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

p = GPIO.PWM(7, 500)  # channel=7 frequency=50Hz
p.start(0)
"""
try:
    while 1:
        for dc in range(0, 101, 1):
            p.ChangeDutyCycle(dc)
            time.sleep(0.01)
        for dc in range(100, -1, -1):
            p.ChangeDutyCycle(dc)
            time.sleep(0.01)
except KeyboardInterrupt:
    pass
"""
lum = 0
try:
    while 1:

        while lum < 99:
            lum+=0.01
            time.sleep(0.1)
            p.ChangeDutyCycle(lum)
        while lum > 1:
            lum-=0.01
            time.sleep(0.1)
            p.ChangeDutyCycle(lum)
except KeyboardInterrupt:
    pass
    
    
p.stop()
GPIO.cleanup()
