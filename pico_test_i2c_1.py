# i2c_scanner.py
# Raspberry Pi Pico (RP2040)
#
# Pin numbers are GPIO Pin numbers not board pins
#   eg: Pin 8 (GPIO 8) is board pin 11
#       Pin 9 (GPIO 9) is board pin 12
#
# I2C primitive methods only available in class machine.SoftI2C

# https://www.raspberrypi.org/forums/viewtopic.php?t=304074

import machine

sda=machine.Pin(8)
scl=machine.Pin(9)
i2c=machine.SoftI2C(sda=sda, scl=scl, freq=100000, timeout=255)
 
print('Start I2C test...')

buf = bytearray(10)

while (True):
    i2c.readinto(buf, False)
    print(buf)
