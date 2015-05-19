#!/usr/bin/python

######################################################
#  ****************************************
#  Neural Network Color Classification    \
#  Using Yocto & Numpy                    /
#  Running KnNN Network                   \
#                                         /
#  Alejandro Enedino Hernandez Samaniego  \
#  alejandro.hernandez@linux.intel.com    /
#  alejandro.hernandez@intel.com          \
#  aehs29@ieee.org                        /
#  ****************************************
######################################################

# Red: Connected to Pin 2 : Linux GPIO = gpio13 : Mux gpio34 = 0
# Green: Connected to Pin 3 : Linux GPIO = gpio14 : Mux gpio16 = 0
# Blue: Connected to Pin 4 : Linux GPIO = gpio6 : Mux gpio36 = 0
# Photoresistor: Connected to ADC0 : iio:device0/in_voltage0_raw

# Classes
# Red = 1
# Green = 2
# Blue = 3
# Nothing = 4

# Imports
import sys
import time
from neural_nets import knnn

# Specify number of neighbors
k=5

# Declare GPIOs
iored = "13"
iogreen = "14"
ioblue = "6"
muxred = "34"
muxgreen = "16"
muxblue = "36"

iolist = []
iolist.append(iored)
iolist.append(iogreen)
iolist.append(ioblue)

muxlist = []
muxlist.append(muxred)
muxlist.append(muxgreen)
muxlist.append(muxblue)

alllist = iolist + muxlist

# Make sure GPIOs are unexported
for i in alllist:
    with open("/sys/class/gpio/unexport", "w") as exportfile:
        exportfile.write(i)
# Export
for i in alllist:
    with open("/sys/class/gpio/export", "w") as exportfile:
        exportfile.write(i)

# I/O Direction
for i in alllist:
    with open("/sys/class/gpio/gpio" + str(i) + "/direction", "w+") as dirfile:
        dirfile.write("out")

# Muxes
for i in muxlist:
    with open("/sys/class/gpio/gpio" + str(i) + "/value", "w+") as muxfile:
        muxfile.write("0")

# Turn Off Everything
for i in iolist:
    with open("/sys/class/gpio/gpio" + str(i) + "/value", "w+") as iofile:
        iofile.write("1")



def turnOn(value):
    if (value == 1):
        io = iored
    elif(value == 2):
        io = iogreen
    elif(value == 3):
        io = ioblue
    elif(value == 4):
	return

    with open("/sys/class/gpio/gpio" + str(io) + "/value", "w+") as iofile:
        iofile.write("0")

def turnOff(value):
    if (value == 1):
        io = iored
    elif(value == 2):
        io = iogreen
    elif(value == 3):
        io = ioblue
    elif(value == 4):
	return

    with open("/sys/class/gpio/gpio" + str(io) + "/value", "w+") as iofile:
        iofile.write("1")

# Create class object
knn_net = knnn("/opt/neural_training", k)
print("Ready")

while True:

    # Read analog value
    A0file = open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw", "r")
    measurement = A0file.readline()
    A0file.close()
    measurement = int(measurement.rstrip())

    # Get probabilities for classes (Call KNN)
    result = knn_net.classify(measurement)

    # Assign Class / Turn on RGB LED accordingly
    turnOn(result)

    # Print some info to make sure we're still alive
    # print 'Measurement:{} Class:{}'.format(measurement,result)
    print 'Class:{}'.format(result)

    # Noop for a while
    time.sleep(2)

    # Turn Off RGB LED
    turnOff(result)
