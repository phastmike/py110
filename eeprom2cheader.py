#!/bin/python

""" M110 GENERATE C HEADER WITH EEPROM DATA
    2021 CT1ENQ
"""

import sys
from motorola import m110 as radius 

if len(sys.argv) != 2:
    print ("Usage: %s <filename>" % sys.argv[0])
    exit(0)

file = sys.argv[1]

print("")
print("- Loading eeprom from binary file '%s'" % file)
radio = radius.m110()
radio.setup_from_file(file)

# Show eeprom content
print("")
radio.show_info()
print("")

tokens = file.split('.')
cheader_file = tokens[0] + '.h'

print("")
print("- Converting to C Header file '%s'" % cheader_file)

try:
    f = open(cheader_file, 'w+')
    f.write("unsigned char rom_init[128] = {\n")
    i = 1
    f.write("   ")
    for byte in radio.mem:
        f.write("0x%02x" % byte)
        if (i < 128):
            f.write(",")
        else:
            f.write("\n};")
        if i % 8 == 0:
            f.write("\n   ")
        i += 1
    f.close()
except OSError as error:
    print('Error: ', error)

