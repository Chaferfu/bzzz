# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 12:53:35 2018

@author: mbazin2
"""

import serial
ser = serial.Serial(0)  # open first serial port
print(ser.portstr)       # check which port was really used
msg = ser.read()
print(msg)                # write a string
ser.close()             # close port
