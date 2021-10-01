import time
from machine import Pin,I2C

I2C_DEVICE = 1
I2C_FREQ = 400000
GPIO_PIN_SDA = 2
GPIO_PIN_SCL = 3
EEPROM_ADDRESS = 0x50
CH_NBYTES = 10
CH1_OFFSET = 0x1B
CH2_OFFSET = 0x25
PRESCALER = 127
PLL_REF_STEP = 0.00625 # 6.25kHz / 0.00625 MHz
RX_FI = 21.4

eeprom = I2C(I2C_DEVICE,scl=Pin(GPIO_PIN_SCL),sda=Pin(GPIO_PIN_SDA),freq=I2C_FREQ)

ch1 = eeprom.readfrom_mem(EEPROM_ADDRESS, CH1_OFFSET, CH_NBYTES)
ch2 = eeprom.readfrom_mem(EEPROM_ADDRESS, CH2_OFFSET, CH_NBYTES)

def get_tx_freq(ch_data):
    tx_a = ch_data[4] >> 1
    tx_n = 0x3ff & ((ch_data[2] << 8) + ch_data[3])
    tx_freq = ((tx_n * PRESCALER) + tx_a) * PLL_REF_STEP
    return tx_freq # In MHz

def get_rx_freq(ch_data):
    rx_a = ch_data[9] >> 1
    rx_n = 0x3ff & ((ch_data[7] << 8) + ch_data[8])
    rx_freq = (((rx_n * PRESCALER) + rx_a) * PLL_REF_STEP) + RX_FI
    return rx_freq # In MHz

def set_tx_freq(ch_data, freqMHz):
    data = bytearray(ch_data)
    freqkHz = freqMHz * 1000
    ft  = freqkHz / 6.25
    N   = 0xe600 | int(ft // 127)
    A   = int(ft % 127) << 1
    data[2] = (N >> 8) & 0xff
    data[3] = N & 0xff
    data[4] = A
    return bytes(data)

def set_rx_freq(ch_data, freqMHz):
    data = bytearray(ch_data)
    freqMHz -= 21.4
    freqkHz = freqMHz * 1000
    ft  = freqkHz / 6.25
    N   = 0x4e00 | int(ft // 127)
    A   = int(ft % 127) << 1
    data[7] = (N >> 8) & 0xff
    data[8] = N & 0xff
    data[9] = A
    return bytes(data)

def to_hex(value):
    return '0x{:02x}'.format(value)

def print_freqs(ch_data):
    print ('RX: {0} MHz TX: {1} MHz'.format(get_rx_freq(ch_data), get_tx_freq(ch_data)))
    
def print_bytes(ch_data):
    print('[', end =' ')
    for b in ch_data:
        print(to_hex(b), end = ' ')
    print(']')
    
def write_bytes(address, ch_offset, data):
    for i in range(10):
        print('Writing to eeprom at address {0}, value {1}'.format(to_hex(ch_offset+i), to_hex(data[i])))
        eeprom.writeto_mem(address, ch_offset+i, bytearray([data[i]]))
        #eeprom.regenerate_checksum()

print_freqs(ch1)
print_bytes(ch1)
print_freqs(ch2)
print_bytes(ch2)

#ch1 = set_rx_freq(ch1,468.800)
#print_freqs_for_channel(ch1)
#ch1 = set_tx_freq(ch1,458.800)
#print_freqs_for_channel(ch1)

#print ('[CH 1] RX: {0} MHz TX: {1} MHz'.format(get_rx_freq(ch1), get_tx_freq(ch1)))
#print ('[CH 2] RX: {0} MHz TX: {1} MHz'.format(get_rx_freq(ch2), get_tx_freq(ch2)))
