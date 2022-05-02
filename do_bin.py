#!/bin/python

from motorola import m110 as radius 

file = 'eeprom_binaries/auchan.bin'

print("MOTOROLA Radius M110 eeprom bin maker ")
print("======================================")
print("Loading eeprom from binary file '%s'" % file)
print("")

radio = radius.m110()
radio.setup_from_file(file)

radio.set_channel_freq(1, 467.825, 467.825);
radio.set_rx_ctcss(radio.CH1_INDEX, 0);
radio.set_tx_ctcss(radio.CH1_INDEX, 0);

radio.set_channel_freq(2, 467.875, 467.875);
radio.set_rx_ctcss(radio.CH2_INDEX, 0);
radio.set_tx_ctcss(radio.CH2_INDEX, 0);

radio.set_timeout(180);
radio.set_rekey(1);

radio.show_info()

radio.save_bytes_to_file('cp2.bin')

