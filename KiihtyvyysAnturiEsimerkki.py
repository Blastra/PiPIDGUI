import smbus
import time
import os

class Lumin():
    myBus=""
    if GPIO.RPI_REVISION == 1:
        myBus=0
    elif GPIO.RPI_REVISION == 2:
        myBus=1
    b = smbus.SMBus(myBus)

    def setUp(self):
        self.b.write_byte_data(0x23,0x16,0x55)
    def getValue(self):
        return self.b.read_byte_data(0x23,0x06)

IntenTestaus = Lumin()
IntenTestaus.setUp()

for a in range(100):
    IntenTestaus.getValueX()
    print("KalastettuArvo = "+str(x))
    time.sleep(0.5)
    #os.system("clear")
