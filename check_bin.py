#!/bin/python

""" M110 CHECK EEPROM BIN FILE
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
