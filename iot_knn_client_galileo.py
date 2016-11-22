######################################################
#  ****************************************
#  IoT Client on Galileo                  \
#  Using Yocto & Machine Learning         /
#                                         \
#                                         /
#  Alejandro Enedino Hernandez Samaniego  \
#  alejandro.hernandez@linux.intel.com    /
#  alejandro.hernandez@intel.com          \
#  aehs29@ieee.org                        /
#  ****************************************
######################################################


# Python Imports
import socket
import sys
from time import sleep
import random
import pyupm_i2clcd as lcd
import mraa


# Set up network 
server='192.168.1.100'
port=8888

# Get Client IP Address
try:
    ip=[(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
except socket.error as msg:
    print msg

# Set up MRAA

btn=mraa.Gpio(5)
btn.dir(mraa.DIR_IN)
temp=mraa.Aio(1)
light=mraa.Aio(0)


# Set up LCD Screen using both upm and MRAA
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
x = mraa.I2c(0)
x.address(0x62)
# Init LCD using MRAA
x.writeReg(0, 0)
x.writeReg(1, 0)
# Send RGB color data
x.writeReg(0x08, 0xAA)
# Red
x.writeReg(0x04, 159)
# Green
x.writeReg(0x03, 0)
# Blue
x.writeReg(0x02, 255)


# Use UPM to manipulate LCD
myLcd.setCursor(0,0)
myLcd.write('%s' % ip)
myLcd.setCursor(1,0)
myLcd.write('Waiting for server')
scrollFlag = False
scrollCount = 0

# Wait for button
while btn.read()==0:
    myLcd.setCursor(0,0)
    myLcd.write('%s' % ip)
    myLcd.setCursor(1,0)
    myLcd.write('Waiting for server')
    myLcd.scroll(scrollFlag)
    sleep(1)
    scrollCount+=1
    if(scrollCount==4):
        scrollFlag = not scrollFlag
        scrollCount=0

# Create socket and connect to server
try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
print 'Socket Created'
s.connect((server , port))
print 'Socket Connected to ' + server

# Loop
while True:
    sleep(1)
    lightval=light.read()
    tempval=temp.read()
    message = '%s,%s' % (lightval,tempval)
    try :
        # Send the whole string
        s.sendall(message)
    except socket.error:
        # Send failed
        print 'Send failed'
        sys.exit()
    # Server replied
    reply = s.recv(4096)
    print reply

    # Write result obtained from server and values read from sensors
    myLcd.clear()
    myLcd.setCursor(0,0)
    myLcd.write(message)
    myLcd.setCursor(1,0)
    myLcd.write(reply)
