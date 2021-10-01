"""I2C EEPROM Emulation
"""

# Standard Library
import time
from machine import Pin, I2C

# Local
from i2c_responder import I2CResponder
from eeprom import M110EEPROM

PIN_LED = 25
LED = Pin(PIN_LED,Pin.OUT)
PIN_MEM_ENABLED = 20
MEM_ENABLED = Pin(PIN_MEM_ENABLED, Pin.IN)

RESPONDER_I2C_DEVICE_ID = 1
RESPONDER_ADDRESS = 0x50
GPIO_RESPONDER_SDA = 2
GPIO_RESPONDER_SCL = 3

I2C_FREQUENCY = 100000

CONTROLLER_I2C_DEVICE_ID = 1
GPIO_CONTROLLER_SDA = 2
GPIO_CONTROLLER_SCL = 3

def main():
    
    # -----------------
    # Initialize M110EEPROM
    # -----------------
    eeprom=M110EEPROM()
    
    # -----------------
    # Initialize Responder
    # -----------------
    i2c_responder = I2CResponder(
        RESPONDER_I2C_DEVICE_ID, sda_gpio=GPIO_RESPONDER_SDA, scl_gpio=GPIO_RESPONDER_SCL, responder_address=RESPONDER_ADDRESS
    )

    print('I2CResponder v' + i2c_responder.VERSION)
    
    while True:       
        if i2c_responder.write_data_is_available():
            LED.high()
            print('----------------------------------------------------------------------------------------------')
            print('   Responder: Getting I2C WRITE data...')
            buffer_in = i2c_responder.get_write_data(8)
            buffer_in_len = len(buffer_in)
            print('   Responder: Received I2C WRITE data : ' + format_hex(buffer_in) + ' length: ' + format_hex(buffer_in_len))
            if buffer_in_len == 1:
                if i2c_responder.read_is_pending():
                    # Probably an memory address
                    val = buffer_in[0]
                    mem_value = eeprom.read_byte(val)
                    print('   Responder: Sending I2C READ data after addressed write: ' + format_hex(mem_value))
                    i2c_responder.put_read_data(mem_value)
                else:
                    printf('   Bus Error? No READ after addressed write...')
            else:
                # Seq. Write?
                print('   Responder: Cannot handle seq read yet!')
            LED.low()
        else:
            if i2c_responder.read_is_pending():
                print ('   Responder READ is pending... Why?')
                val = eeprom.read()
                i2c_responder.put_read_data(val)
                print ('   Responder READ data was sent: ' + format_hex(val))
            else:
                time.sleep(0.1)
        # ended if - loop again
        
def format_hex(_object):
    """Format a value or list of values as 2 digit hex."""
    try:
        values_hex = [to_hex(value) for value in _object]
        return '[{}]'.format(', '.join(values_hex))
    except TypeError:
        # The object is a single value
        return to_hex(_object)

def to_hex(value):
    return '0x{:02X}'.format(value)


if __name__ == "__main__":
    main()
