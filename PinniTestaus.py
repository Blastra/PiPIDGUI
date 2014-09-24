import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

p = GPIO.PWM(7,

p.start(1)

input("Press return to stop:")

p.stop()

GPIO.cleanup()


