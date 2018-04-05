# Ce code ne m'appartient pas et vient de stackoverflow, à l'adresse
# https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python#14224477

import sys
import glob
import serial
import serial.tools.list_ports

def list_ports() :
    list = serial.tools.list_ports.comports()
    connected = []
    for element in list:
        connected.append(element.device)
    print("Connected COM ports: " + str(connected))
    return

if __name__ == "__main__" :
    list_ports()
