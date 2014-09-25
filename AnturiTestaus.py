import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

channel = 3

GPIO.setup(channel,GPIO.I2C)

incoming = GPIO.input(channel)

#To wait for a button press by polling in a loop:
#while GPIO.input(channel) == GPIO.LOW:
#    time.sleep(0.01)  # wait 10 ms to give CPU chance to do other things
#counter=100

#print(dir(incoming))

#print(incoming.real())

counter = 100

while counter > 0:
    time.sleep(0.1)
    counter-=1
    print(GPIO.input(channel))

