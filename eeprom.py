"""EEPROM Emulation
    - Implements Sequencial read/write
    - Implements byte read/write at given location

    We don't initialize the eeprom to the default 0xFF on all bytes
    because our particular case has all bytes to 0x00 by default so
    it would be lost time to be changing bytes to 0xFF and right
    back to 0X00, but for generalization it would be required tough.

    2021 José Miguel Fonte
"""

import math
import enum

class EEPROM:
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

    def reset(self):
        self.__offset = 0

    def offset_inc(self):
        self.__offset += 1
        if self.__offset >= self.__nbytes:
            self.reset()
        
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
    
class TxAdmit(enum.Enum):
    MONITOR = 0
    ALWAYS = 4
    NO_CARRIER = 5
    PL_NOCAR = 7

class ChannelSpacing(enum.Enum):
    isUNKNOWN= 0
    is25kHz = 1
    is20kHz = 2
    is12_5kHz = 3

class Band(enum.Enum):
    INVALID = 0
    UHF_LOW_403_433MHz = 12
    UHF_X1_RX_LOW_TX_HIGH = 13
    UHF_X2_RX_HIGH_TX_LOW = 14
    UHF_HIGH_438_470MHz = 15

class Power(enum.Enum):
    LOW = 0
    HIGH = 1

class M110EEPROM(EEPROM):
    EEPROM_SIZE = 128
    CHECKSUM_INDEX = 0x0F
    CH1_INDEX = 0x1B
    CH2_INDEX = 0x25
    PRESCALER = 127
    TOT_INDEX = 0x18
    REKEY_INDEX = 0x19
    DEF_INDEX = 0x0A
    PLL_REF_STEP = 0.00625 # 6.25kHz / 0.00625 MHz
    RX_FI = 21.4
    
    def __init__(self):
        super(M110EEPROM, self).__init__(self.EEPROM_SIZE)
        
    def setup_from_bytes(self, eeprom_bytes):
        if len(eeprom_bytes) == self.EEPROM_SIZE:
            for i in range(self.EEPROM_SIZE):
                self.mem[i] = eeprom_bytes[i]
        else:
            print('M110EEPROM::ERROR:setup_from_bytes:: size incorrect')

    def setup_from_file(self, filename):
        try:
            f = open(filename, 'rb')
        except OSError as error:
            print('setup_from_file: ', error)
        else:
            content = f.read()
            f.close()
            self.setup_from_bytes(content)

    def save_bytes_to_file(self, filename):
        try:
            f = open(filename, 'wb')
            f.write(self.mem)
            f.close()
        except OSError as error:
            print('setup_from_file: ', error)

    def get_checksum(self):
        return self.mem[self.CHECKSUM_INDEX]
    
    def set_checksum(self, checksum):
        if (checksum >= 0x00 and checksum <= 0xFF):
            self.mem[self.CHECKSUM_INDEX] = checksum
    
    def regenerate_checksum(self):
        sum = 0
        self.set_checksum(0xFF)
        for i in range(0x30):
            #Not using read byte method because its not a real read
            sum+=self.mem[i]
        # Remove byte overflow
        val = sum & 0xFF
        # Checksum8 Two's complement
        self.mem[self.CHECKSUM_INDEX] = (0x100 - val) & 0xFF
        #print ("sum=0x%04x" % (sum))
        #print ("val=0x%02x" % (val))
        #print ("Regenerated Checksum @ 0x0F = 0x%02x" % self.get_checksum())
        
        
    def set_channel_freq(self, ch, freqMHzTx, freqMHzRx):
        if ch == 1:
            ch_index = self.CH1_INDEX
        else:
            if ch == 2:
                ch_index = self.CH2_INDEX
            else:
                return
        freqkHzTx = freqMHzTx * 1000
        ft  = freqkHzTx / 6.25
        N   = 0xe600 | int(ft // 127)
        A   = int(ft % 127) << 1
        self.mem[ch_index+2] = (N >> 8) & 0xff
        self.mem[ch_index+3] = N & 0xff
        self.mem[ch_index+4] = A
        freqMHzRx -= self.RX_FI
        freqkHzRx = freqMHzRx * 1000
        ft  = freqkHzRx / 6.25
        N   = 0x4e00 | int(ft // 127)
        A   = int(ft % 127) << 1
        self.mem[ch_index+7] = (N >> 8) & 0xff
        self.mem[ch_index+8] = N & 0xff
        self.mem[ch_index+9] = A
        # Regenerate checkum
        self.regenerate_checksum()

    def get_tx_freq(self, ch_index):
        if (ch_index != self.CH1_INDEX and ch_index != self.CH2_INDEX):
            return 0
        tx_a = self.mem[ch_index+4] >> 1
        tx_n = 0x3ff & ((self.mem[ch_index+2] << 8) + self.mem[ch_index+3])
        tx_freq = ((tx_n * self.PRESCALER) + tx_a) * self.PLL_REF_STEP
        return tx_freq # In MHz

    def get_rx_freq(self, ch_index):
        rx_a = self.mem[ch_index+9] >> 1
        rx_n = 0x3ff & ((self.mem[ch_index+7] << 8) + self.mem[ch_index+8])
        rx_freq = (((rx_n * self.PRESCALER) + rx_a) * self.PLL_REF_STEP) + self.RX_FI
        return rx_freq # In MHz

    def get_tx_ctcss(self, ch_index):
        if (ch_index != self.CH1_INDEX and ch_index != self.CH2_INDEX):
            return 0
        tx_a = self.mem[ch_index+4] >> 1
        tone = self.mem[ch_index] << 8
        tone += self.mem[ch_index+1]
        tone = tone * 0.125233645
        integer = int(tone)
        decimal = math.ceil((tone - integer) * 10) / 10
        tone = integer + decimal
        return tone

    def set_tx_ctcss(self, ch_index, tone):
        if (ch_index != self.CH1_INDEX and ch_index != self.CH2_INDEX):
            return
        tx_a = self.mem[ch_index+4] >> 1
        t = tone / 0.125233645
        decimal = t - int(t)
        if decimal >= 0.5:
            t+=1
        n = int(t)
        #print('tx ctcss integer ', hex(n))
        self.mem[ch_index] = (n >> 8) & 0xFF
        self.mem[ch_index+1] = n & 0xFF
        self.regenerate_checksum()

    def get_rx_ctcss(self, ch_index):
        if (ch_index != self.CH1_INDEX and ch_index != self.CH2_INDEX):
            return 0
        tone = self.mem[ch_index+5] << 8
        tone += self.mem[ch_index+6]
        tone = tone * 0.016365413
        integer = int(tone)
        decimal = math.ceil((tone - integer) * 100)
        decimal = int(decimal/10) / 10
        tone = integer + decimal
        return tone

    def set_rx_ctcss(self, ch_index, tone):
        if (ch_index != self.CH1_INDEX and ch_index != self.CH2_INDEX):
            return
        t = tone / 0.016365413
        decimal = t - int(t)
        if decimal >= 0.5:
            t+=1
        n = int(t)
        #print('tx ctcss integer ', hex(n))
        self.mem[ch_index+5] = (n >> 8) & 0xFF
        self.mem[ch_index+6] = n & 0xFF
        self.regenerate_checksum()

    def get_timeout(self):
        return self.mem[self.TOT_INDEX] * 5

    def set_timeout(self, timeout):
        if timeout % 5 == 0:
            self.mem[self.TOT_INDEX] = timeout / 5
            self.regenerate_checksum()
        else:
            print("set_timeout::invalid timeout value")

    def get_rekey(self):
        return self.mem[self.REKEY_INDEX]

    def set_rekey(self, rekey):
        self.mem[self.REKEY_INDEX] = rekey 
        self.regenerate_checksum()

    def get_clock_shift(self, ch_index):
        if (ch_index != self.CH1_INDEX and ch_index != self.CH2_INDEX):
            return 0
        return self.mem[ch_index+7] & 0x80 != 0

    def set_clock_shift(self, ch_index, clock_shift):
        if (ch_index != self.CH1_INDEX and ch_index != self.CH2_INDEX):
            return
        if (clock_shift == 0):
            self.mem[ch_index+7] &= 0x7F
        else:
            self.mem[ch_index+7] |= 0x80
        self.regenerate_checksum()

    def get_monitor_enable(self, ch_index):
        if (ch_index != self.CH1_INDEX and ch_index != self.CH2_INDEX):
            return 0
        return self.mem[ch_index+7] & 0x08 != 0
    
    def set_monitor_enable(self, ch_index, enable):
        if (ch_index != self.CH1_INDEX and ch_index != self.CH2_INDEX):
            return
        if (enable == 0):
            self.mem[ch_index+7] &= 0xF7
        else:
            self.mem[ch_index+7] |= 0x08
        self.regenerate_checksum()

    def get_tx_admit(self, ch_index):
        if (ch_index != self.CH1_INDEX and ch_index != self.CH2_INDEX):
            return TxAdmit(0)
        txa = self.mem[ch_index+2]
        txa = (txa >> 3) & 0x07
        return TxAdmit(txa)

    def set_tx_admit(self, ch_index, tx_admit):
        self.mem[ch_index+2] = 0xc6 + (tx_admit.value << 3)
        self.regenerate_checksum()

    def get_power(self):
        return Power(int(self.mem[self.DEF_INDEX] >> 6 == 0x03))

    def set_power(self, power):
        if (power == Power.LOW):
            self.mem[self.DEF_INDEX] &= 0x3F
            self.regenerate_checksum()
        elif (power == Power.HIGH):
            self.mem[self.DEF_INDEX] |= 0xC0
            self.regenerate_checksum()
        else:
            print('set_power::Invalid power value')

    def get_channel_spacing(self):
        return ChannelSpacing((self.mem[self.DEF_INDEX] >> 4) & 0x03)

    def set_channel_spacing(self, ch_spacing):
        self.mem[self.DEF_INDEX] &= 0xcf
        self.mem[self.DEF_INDEX] += ch_spacing.value << 4
        self.regenerate_checksum()

    def get_band(self):
        return Band(self.mem[self.DEF_INDEX] & 0x0F)

    def set_band(self, band):
        self.mem[self.DEF_INDEX] &= 0xF0
        self.mem[self.DEF_INDEX] += band.value
        self.regenerate_checksum()

    def get_serial(self):
        return bytes(self.mem[0:10])

    def set_serial(self, serial):
        if (len(serial) != 10):
            return
        i=0
        for c in serial:
            self.mem[i] = ord(c)
            i+=1
        self.regenerate_checksum()

    def show_channels(self):
        print ('==============================================================')
        print ('CH.1  RX : %.05f MHz (%.1f Hz) TX: %.05f MHz (%.1f Hz)' % (self.get_rx_freq(self.CH1_INDEX), self.get_rx_ctcss(self.CH1_INDEX), self.get_tx_freq(self.CH1_INDEX), self.get_tx_ctcss(self.CH1_INDEX)))
        print ('         : ClockShift %d Monitor %d %s' % (self.get_clock_shift(self.CH1_INDEX), self.get_monitor_enable(self.CH1_INDEX), self.get_tx_admit(self.CH1_INDEX)))
        print ('')
        print ('CH.2  RX : %.05f MHz (%.1f Hz) TX: %.05f MHz (%.1f Hz)' % (self.get_rx_freq(self.CH2_INDEX), self.get_rx_ctcss(self.CH2_INDEX), self.get_tx_freq(self.CH2_INDEX), self.get_tx_ctcss(self.CH2_INDEX)))
        print ('         : ClockShift %d Monitor %d %s' % (self.get_clock_shift(self.CH2_INDEX), self.get_monitor_enable(self.CH2_INDEX), self.get_tx_admit(self.CH2_INDEX)))
        print ('==============================================================')

    def show_info(self):
        print ('============================ M110 ============================')
        print ('SERIAL   : %s' % self.get_serial().decode("utf-8"))
        print ('BAND     : %s' % self.get_band())
        print ('BANDWIDTH: %s' % self.get_channel_spacing())
        print ('POWER    : %s' % self.get_power())
        print ('==============================================================')
        print ('TIMEOUT  : %d sec.' % self.get_timeout())
        print ('REKEY    : %d sec.'  % self.get_rekey())
        print ('==============================================================')
        print ('CH.1  RX : %.05f MHz (%.1f Hz) TX: %.05f MHz (%.1f Hz)' % (self.get_rx_freq(self.CH1_INDEX), self.get_rx_ctcss(self.CH1_INDEX), self.get_tx_freq(self.CH1_INDEX), self.get_tx_ctcss(self.CH1_INDEX)))
        print ('         : ClockShift %d Monitor %d %s' % (self.get_clock_shift(self.CH1_INDEX), self.get_monitor_enable(self.CH1_INDEX), self.get_tx_admit(self.CH1_INDEX)))
        print ('')
        print ('CH.2  RX : %.05f MHz (%.1f Hz) TX: %.05f MHz (%.1f Hz)' % (self.get_rx_freq(self.CH2_INDEX), self.get_rx_ctcss(self.CH2_INDEX), self.get_tx_freq(self.CH2_INDEX), self.get_tx_ctcss(self.CH2_INDEX)))
        print ('         : ClockShift %d Monitor %d %s' % (self.get_clock_shift(self.CH2_INDEX), self.get_monitor_enable(self.CH2_INDEX), self.get_tx_admit(self.CH2_INDEX)))
        print ('==============================================================')
        print ('CHECKSUM : 0x%02X (%d)' % (self.get_checksum(), self.get_checksum()))  
        print ('==============================================================')

class M110Channel:

    def __init__(self):
        self.freq_tx = 0
        self.freq_rx = 0
        self.ctcss_tx = 0.0
        self.ctcss_rx = 0.0
        self.clk_shift = False
        self.transmit_admit = 0
        self.monitor_inhibit = False
