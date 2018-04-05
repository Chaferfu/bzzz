# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 12:51:08 2018

@author: mbazin2
"""

import serial
ser = serial.Serial(0)  # open first serial port
print(ser.portstr)       # check which port was really used
ser.write("abaaba")      # write a string
ser.close()             # close port
