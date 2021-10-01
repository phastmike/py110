import time
from eeprom import *
from machine import Pin,I2C

I2C_DEVICE = 1
I2C_FREQ = 100000
GPIO_PIN_SDA = 2
GPIO_PIN_SCL = 3
EEPROM_ADDRESS = 0x50

eeprom = I2C(I2C_DEVICE,scl=Pin(GPIO_PIN_SCL),sda=Pin(GPIO_PIN_SDA),freq=I2C_FREQ)
m110 = M110EEPROM()
m110.setup_from_bytes(eeprom.readfrom_mem(EEPROM_ADDRESS, 0, m110.EEPROM_SIZE))

def commit_to_device(data):
    # M110 only uses 48 bytes
    for i in range(0x30):
        print('Writing to eeprom at address 0x%02X: data 0x%02X' % (i, data[i]))
        eeprom.writeto_mem(EEPROM_ADDRESS, i, data[i:i+1])
        time.sleep(0.1)
        
print ('[CH 1] TX: %.03f MHz RX: %.03f MHz' % (m110.get_tx_freq(m110.CH1_INDEX), m110.get_rx_freq(m110.CH1_INDEX)))
print ('[CH 2] TX: %.03f MHz RX: %.03f MHz' % (m110.get_tx_freq(m110.CH2_INDEX), m110.get_rx_freq(m110.CH2_INDEX)))
print ('[CHKSUM] : 0x%02X (%d)' % (m110.get_checksum(), m110.get_checksum()))  
