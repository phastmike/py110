#!/bin/python

""" M110 EEPROM TESTS
    2021 CT1ENQ
"""

from motorola import m110 as radius

def sweep_tones_test(m110):
    print("- Sweep set and test all ctcss tones")

    ctcss_list = [ 67.0, 69.3,
                   71.9, 74.4, 77.0, 79.7,
                   82.5, 85.4, 88.5,
                   91.5, 94.8, 97.4,
                   100.0, 103.5, 107.2,
                   110.9, 114.8, 118.8,
                   123.0, 127.3,
                   131.8, 136.5,
                   141.3, 146.2,
                   151.4, 156.7, 159.8,
                   162.2, 165.5, 167.9,
                   171.3, 173.8, 177.3, 179.9,
                   183.5, 186.2, 189.9,
                   192.8, 196.6, 199.5,
                   203.5, 206.5,
                   210.7, 218.1,
                   225.7, 229.1,
                   233.6,
                   241.8,
                   250.3, 254.1 ]

    ok = 0
    failed = 0

    # CHANNEL 1
    for tone in ctcss_list:
        #print ("- Checking tone ", tone)
        m110.set_rx_ctcss(m110.CH1_INDEX, tone)
        ctone = m110.get_rx_ctcss(m110.CH1_INDEX)
        if (tone == ctone):
            result = "OK"
            ok += 1
        else:
            result = "FAIL"
            failed += 1
        #print("   RX => Wrote %.1f = Read %.1f ? %s" % (tone, ctone, result))
        m110.set_tx_ctcss(m110.CH1_INDEX, tone)
        ctone = m110.get_rx_ctcss(m110.CH1_INDEX)
        if (tone == ctone):
            result = "OK"
            ok += 1
        else:
            result = "FAIL"
            failed += 1

    # CHANNEL 2
    for tone in ctcss_list:
        #print ("- Checking tone ", tone)
        m110.set_rx_ctcss(m110.CH2_INDEX, tone)
        ctone = m110.get_rx_ctcss(m110.CH2_INDEX)
        if (tone == ctone):
            result = "OK"
            ok += 1
        else:
            result = "FAIL"
            failed += 1
        #print("   RX => Wrote %.1f = Read %.1f ? %s" % (tone, ctone, result))
        m110.set_tx_ctcss(m110.CH2_INDEX, tone)
        ctone = m110.get_rx_ctcss(m110.CH2_INDEX)
        if (tone == ctone):
            result = "OK"
            ok += 1
        else:
            result = "FAIL"
            failed += 1
        #print("   TX => Wrote %.1f = Read %.1f ? %s" % (tone, ctone, result))

        #print("")
    print("   Total: %d ok, %d failed" % (ok, failed))

def test_clock_shift(m110):
    print("- Test CH1 and CH2 ClockShift") 
    m110.set_clock_shift(m110.CH1_INDEX, 1)
    m110.set_clock_shift(m110.CH2_INDEX, 1)
    c1 = m110.get_clock_shift(m110.CH1_INDEX)
    c2 = m110.get_clock_shift(m110.CH2_INDEX)
    if (c1 == 1 and c2 == 1):
        print ('   Set OK')
    else:
        print ('   Set FAILED')

    m110.set_clock_shift(m110.CH1_INDEX, 0)
    m110.set_clock_shift(m110.CH2_INDEX, 0)
    c1 = m110.get_clock_shift(m110.CH1_INDEX)
    c2 = m110.get_clock_shift(m110.CH2_INDEX)
    if (c1 == 0 and c2 == 0):
        print ('   Unset OK')
    else:
        print ('   Unset FAILED')

def test_monitor_enable(m119):
    print("- Test CH1 and CH2 Monitor Enable") 
    m110.set_monitor_enable(m110.CH1_INDEX, 0)
    m110.set_monitor_enable(m110.CH2_INDEX, 0)
    c1 = m110.get_monitor_enable(m110.CH1_INDEX)
    c2 = m110.get_monitor_enable(m110.CH2_INDEX)
    if (c1 == 0 and c2 == 0):
        print ('   Unset OK')
    else:
        print ('   unset FAILED')
    m110.set_monitor_enable(m110.CH1_INDEX, 1)
    m110.set_monitor_enable(m110.CH2_INDEX, 1)
    c1 = m110.get_monitor_enable(m110.CH1_INDEX)
    c2 = m110.get_monitor_enable(m110.CH2_INDEX)
    if (c1 == 1 and c2 == 1):
        print ('   Set OK')
    else:
        print ('   Set FAILED')

def test_tx_admit(m119):
    ok = 0
    failed = 0
    print("- Test CH1 and CH2 TxAdmit") 
    for val in radius.TxAdmit:
        m110.set_tx_admit(m110.CH1_INDEX, val)
        if (m110.get_tx_admit(m110.CH1_INDEX) == val):
            ok += 1
            #print ("   CH1 %s OK" % val)
        else:
            failed += 1
            #print ("   CH1 %s FAILED" % val)
        m110.set_tx_admit(m110.CH2_INDEX, val)
        if (m110.get_tx_admit(m110.CH2_INDEX) == val):
            ok += 1
            #print ("   CH2 %s OK" % val)
        else:
            failed += 1
            #print ("   CH2 %s FAILED" % val)
    print ("   Total: %d ok, %d failed" % (ok, failed))
    
########################################################################

#SETUP
print("")
print("- Setup")
m110 = radius.m110()
file = './eeprom_binaries/24c01_CP_01.bin'
print("   from file '%s'" % file)
m110.setup_from_file(file)

# START
print("")
m110.show_info()

print("")
test_clock_shift(m110)

print("")
test_monitor_enable(m110)

print("")
sweep_tones_test(m110)

print("")
test_tx_admit(m110)

#print("")
#m110.show_channels()

print("")
