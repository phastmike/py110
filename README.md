# Python Tools for Motorola M110

While prototyping and debugging Motorola's M110 some
python tools were developed:

- check_bin.py
- do_bin.py
- eeprom2cheader.py
- menu.py
- tests_m110.py

There are also a couple folders:

- eeprom_binaries
- motorola

Next, follows an explanation of the above files and folders:

## check_bin.py

Outputs to the screen the information of a Motorola eeprom 
binary data file (retrieved with a eeprom reader - eg: TL866ii plus)

```
[...]$ ./check_bin.py eeprom_binaries/auchan.bin 


- Loading eeprom from binary file 'eeprom_binaries/auchan.bin'

============================ M110 ============================
SERIAL   : RSA1525EZA
BAND     : Band.UHF_HIGH_438_470MHz
BANDWIDTH: ChannelSpacing.is25kHz
POWER    : Power.HIGH
==============================================================
TIMEOUT  : 165 sec.
REKEY    : 2 sec.
==============================================================
CH.1  RX : 444.36250 MHz (107.2 Hz) TX: 444.36250 MHz (79.6 Hz)
         : ClockShift 0 Monitor 1 TxAdmit.ALWAYS
==============================================================
CH.2  RX : 467.87500 MHz (79.7 Hz) TX: 458.50000 MHz (79.6 Hz)
         : ClockShift 0 Monitor 1 TxAdmit.ALWAYS
==============================================================
CHECKSUM : 0x48 (72) CALCULATED AS 0x48
==============================================================
```

## do_bin.py

Creates, programmatically, a eeprom binary (.bin) file. User should edit the
script and change the values as needed. The resulting file could be programmed
into an eeprom via a programmer.

## eeprom2cheader.py

Creates a header (.h) file to be used by a c program with an array 
which is initialized with the eeprom binary file contents. Can be 
used as a starting point (default values) for a the eeprom content.

Output example:

```
unsigned char rom_init[128] = {
   0x52,0x53,0x41,0x31,0x35,0x32,0x35,0x45,
   0x5a,0x41,0xdf,0x02,0x00,0x00,0x00,0x48,
   0x58,0x00,0x50,0x16,0x81,0x12,0x01,0x02,
   0x21,0x02,0x20,0x02,0x7c,0xe6,0x2f,0xd2,
   0x19,0x96,0x4e,0x14,0xdc,0x02,0x7c,0xe6,
   0x41,0xa2,0x13,0x06,0x4e,0x32,0x7c,0x00,
   0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
   0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
   0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
   0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
   0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
   0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
   0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
   0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
   0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
   0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00
};
```

## menu.py

Interactive console to read and edit a eeprom binary file. **Not finished yet...**

```
[...]$ ./menu.py eeprom_binaries/auchan.bin 
MOTOROLA Radius M110 Eeprom editor
==================================
Loading eeprom from binary file 'eeprom_binaries/auchan.bin'

Command: Help, Load, Set, shoW, Quit? 
```

## tests_m110.py

Runs tests on motorola python class located in motorola folder.


## eeprom_binaries folder

This folder contains some eeprom binaries, some read from radio some generated.
It may also include header files generated with `eeprom2cheader.py`.

## motorola folder

This folder contains python classes and methods that replicate M110 firmare operations
with a real eeprom but operate with an array that represents an eeprom.

Composed by 2 files, `eeprom.py` and `m110.py`.