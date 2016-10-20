######################################################
#  ****************************************
#  Edison Bluetooth Client Using Python   \
#                                         /
#  Alejandro Enedino Hernandez Samaniego  \
#  alejandro.hernandez@linux.intel.com    /
#  alejandro.hernandez@intel.com          \
#  aehs29@ieee.org                        /
#  ****************************************
######################################################

#! /usr/bin/python
import sys
import bluetooth as bt

# Get the MAC Address from cmdline
# This should be checked for format errors #ToDo
server_addr = str(sys.argv[1])
#bd_addr = "AA:BB:CC:DD:EE:FF"

# Connect to server
port = 29
sock=bt.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((server_addr, port))

# Get new value and send it, otherwise exit
line = ""
print "Please input a PWM value:"
while("exit" not in line):
  line = sys.stdin.readline()
  sock.send(line)
sock.close()
