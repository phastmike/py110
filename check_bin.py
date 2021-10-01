#!/bin/python

""" M110 CHECK EEPROM BIN FILE
    2021 CT1ENQ
"""

import sys
from eeprom import *

if len(sys.argv) != 2:
    print ("Usage: %s <filename>" % sys.argv[0])
    exit(0)

file = sys.argv[1]

print("")
print("- Loading eeprom from binary file '%s'" % file)
m110 = M110EEPROM()
m110.setup_from_file(file)

# Show eeprom content Show eeprom contentss 
print("")
m110.show_info()
print("")
