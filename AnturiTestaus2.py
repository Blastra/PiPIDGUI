import time
import smbus as sb
import RPi.GPIO as RPIO

bus = sb.SMBus(1)

#DEVICE_ADDRESS = 0x23

luettu = bus.read_i2c_block_data(0x03,0x1b)
print(luettu)
luettu = bus.read_i2c_block_data(0x04,0x1b)
print(luettu)
luettu = bus.read_i2c_block_data(0x05,0x1b)
print(luettu)
luettu = bus.read_i2c_block_data(0x10,0x1b)
print(luettu)
luettu = bus.read_i2c_block_data(0x11,0x1b)
print(luettu)
luettu = bus.read_i2c_block_data(0x21,0x1b)
print(luettu)
luettu = bus.read_i2c_block_data(0x23,0x02)
print(luettu)
luettu = bus.read_i2c_block_data(0x24,0x1b)
print(luettu)
luettu = bus.read_i2c_block_data(0x25,0x1b)
print(luettu)
luettu = bus.read_i2c_block_data(0x33,0x1b)
print(luettu)



print(luettu)


#RPIO.setmode(RPIO.BOARD)
#RPIO.setup(3, RPIO.IN)

#input_value = RPIO.input(3)
#print(input_value)
"""
try:
    RPIO.cleanup()
except:
    pass
"""
