"""EEPROM Emulation
    - Implements Sequencial read/write
    - Implements byte read/write at given location

    We don't initialize the eeprom to the default 0xFF on all bytes
    because our particular case has all bytes to 0x00 by default so
    it would be lost time to be changing bytes to 0xFF and right
    back to 0X00, but for generalization it would be required tough.

    2021 José Miguel Fonte
"""

class eeprom:
    VERSION = "0.0.1"

    def __init__(self, size_in_bytes=128):
        """Initialize.

        Args:
            size_in_bytes (int, optional): The eeprom size in bytes, not bits, eg. 1k = 128 bytes)
            if no size is defined, default size is 1k (128 bytes)
        """
        self.__offset = 0
        self.__nbytes = size_in_bytes
        self.mem = bytearray(self.__nbytes)
        self.mem = [0xff for i in range(self.__nbytes)]

    def reset(self):
        self.__offset = 0

    def offset_inc(self):
        self.__offset += 1
        if self.__offset >= self.__nbytes:
            self.reset()

    def get_size(self):
        return self.__nbytes
        
    def read(self):
        val = self.mem[self.offset]
        self.offset_inc()
        return val
    
    def write(self, value):
        self.mem[self.offset] = value
        self.offset_inc()
        
    def read_byte(self, address):
        if address >= 0 and address < self.__nbytes:
            self.__offset = address
            self.offset_inc()
            return self.mem[address]
        else:
            return None

    def write_byte(self, address, value):
        if value >= 0 and value < 255 and address >= 0 and address < self.__nbytes:
            self.__offset = address
            self.write(value)
            self.offset_inc()
    
