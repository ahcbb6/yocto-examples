######################################################
#  ****************************************
#  Bluetooth Server on Edison Using Python \
#                                          /
#  Alejandro Enedino Hernandez Samaniego   \
#  alejandro.hernandez@linux.intel.com     /
#  alejandro.hernandez@intel.com           \
#  aehs29@ieee.org                         /
#  ****************************************
######################################################

#! /usr/bin/python

import bluetooth as bt
import mraa

# Set up Bluetooth Server
server=bt.BluetoothSocket(bluetooth.RFCOMM)
port = 29
server.bind(("",port))

# Start Listening for New Connections (1)
# Should potentially use several tasks #ToDo
server.listen(1)
print "Listening for new connections on port %s" % port

client,addr = server.accept()
print "Accepted connection from %s " % addr
print "Waiting for new PWM value..."

# Set up MRAA
pwm_pin = mraa.Pwm(9)
pwm_pin.enable(True)
data=0

# Wait for Data (Loop)
while(data!="exit"):
  data = client.recv(1024)
  print "[Debug] Received [%s]" % data
  try:
    value = float(data)
  except ValueError:
    break
  # Use received value for PWM
  pwm_pin.write(float(data))

# Close Socket
print "Server is exiting..."
client.close()
server.close()
