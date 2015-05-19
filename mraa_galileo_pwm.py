######################################################
#  ****************************************
#  MRAA Testing PWM & GPIOs Using Python  \
#                                         /
#  Alejandro Enedino Hernandez Samaniego  \
#  alejandro.hernandez@linux.intel.com    /
#  alejandro.hernandez@intel.com          \
#  aehs29@ieee.org                        /
#  ****************************************
######################################################

# Circuit on Galileo Gen 2

# Red: Connected to Pin 2 : Linux GPIO = gpio13 : Mux gpio34 = 0
# Green: Connected to Pin 3 : Linux GPIO = gpio14 : Mux gpio16 = 0
# Blue: Connected to Pin 4 : Linux GPIO = gpio6 : Mux gpio36 = 0
# PWM LED: Connected to Pin 5

import mraa
import time

# Delcare GPIOs
r=mraa.Gpio(2)
g=mraa.Gpio(3)
b=mraa.Gpio(4)
r.dir(mraa.DIR_OUT)
g.dir(mraa.DIR_OUT)
b.dir(mraa.DIR_OUT)

# Delcare PWM
z = mraa.Pwm(5)
z.enable(True)

# Binary counter for Loop
# There are better ways of doing this
i=1
print "Starting Loop"
while(i<8):
  if (i==0):
    r.write(1)
    g.write(1)
    b.write(1)
  if (i==1):
    r.write(1)
    g.write(1)
    b.write(0)
  elif(i==2):
    r.write(1)
    g.write(0)
    b.write(1)
  elif(i==3):
    r.write(1)
    g.write(0)
    b.write(0)
  elif(i==4):
    r.write(0)
    g.write(1)
    b.write(1)
  elif(i==5):
    r.write(0)
    g.write(1)
    b.write(0)
  elif(i==6):
    r.write(0)
    g.write(0)
    b.write(1)
  elif(i==7):
    r.write(0)
    g.write(0)
    b.write(0)

  # Print actual Loop
  print "Loop %s" % i

  for j in range(50):
     # Increment PWM
     z.write(j*0.001*i)

     # Sleep for the sake of human sight
     time.sleep(0.03)

     # Print values every now and then
     if(j%10==0):
       print "Pwm %s" % z.read()
  i+=1

  # Restart
  z.write(0.0)
  print "Sleeping"
  time.sleep(0.5)
  if(i==8):
    i=1
