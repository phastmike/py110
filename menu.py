#!/bin/python

""" M110 EEPROM BIN FILE EDITOR
    2021 CT1ENQ
"""

import sys
from motorola import m110 as radius 

"""Command functions
==============================================================================
"""

def cmd_help():
    print("   Help...")

def cmd_show(m110):
    m110.show_info()

def cmd_exit():
    exit()

"""
==============================================================================
"""

if len(sys.argv) != 2:
    print ("Usage: %s <filename>" % sys.argv[0])
    exit(0)

file = sys.argv[1]

print("MOTOROLA Radius M110 Eeprom editor")
print("==================================")
print("Loading eeprom from binary file '%s'" % file)
print("")

radio = radius.m110()
radio.setup_from_file(file)

while (True):
    option = input("Command: Help, Load, Set, shoW, Quit? ")
    args = option.split()
    if (len(args) > 0):
        if (args[0] == 'load' or args[0] == 'l') and len(args) == 2:
            radio.setup_from_file(args[1])
        elif (args[0] == 'set' or args[0] == 's'):
            if len(args) > 3:
                if (args[1] == 'global' or args[1] == 'g'):
                    if args[2] == 'serial':
                        radio.set_serial(args[3])
                    elif args[2] == 'power':
                        if args[3] == 'l':
                            radio.set_power(radius.Power.LOW)
                        elif args[3] == 'h':
                            radio.set_power(radius.Power.HIGH)
                    else:
                        print(" * Unknown option! Try again...")
                else:         
                    print(" * Unknown option! Try again...")
            else:
                print(" * Invalid option! Try again...")
        elif option == 'quit' or option == 'q':
            cmd_exit()
        elif option == 'show' or option == 'w':
            cmd_show(radio)
        elif option == 'help' or option == 'h':
            cmd_help()
        else:
            print(" * Invalid option! Try again...")
    else:
        print(" * Invalid option! Try again...")


