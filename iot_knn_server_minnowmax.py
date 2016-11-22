######################################################
#  ****************************************
#  Cloud server on Minnowboard Max        \
#  Using Yocto                            /
#                                         \
#                                         /
#  Alejandro Enedino Hernandez Samaniego  \
#  alejandro.hernandez@linux.intel.com    /
#  alejandro.hernandez@intel.com          \
#  aehs29@ieee.org                        /
#  ****************************************
######################################################

# Classify an input obtained from a client over the network
# using the K-Nearest-Neighbors algorithm

import socket
import sys
import mraa
from thread import *
import numpy as np
from StringIO import StringIO



# Specify number of neighbors
k=3
n=0
traindata=''

# LEDs on the Calamari Lure
rl = mraa.Gpio(21)
gl = mraa.Gpio(23)
bl = mraa.Gpio(26)

leds = [rl,gl,bl]

def turnOn(index):
    leds[index].write(1)

def turnOff(index):
    leds[index].write(0)

def train(trainfile,k):
        global traindata
        global n
	# Read Input Files (Training) and assign variables
        trainstr = open(trainfile, "r").read()
        traindata = np.genfromtxt(StringIO(trainstr), delimiter = ",")
        n = traindata.shape[0]

# Initialize resources

for led in leds:
    led.dir(MRAA_GPIO_OUT)    # 0 = MRAA_GPIO_OUT     see http://iotdk.intel.com/docs/master/mraa/gpio_8h.html#afcfd0cb57b9f605239767c4d18ed7304


def knn(invals):
        # Initialize class counters
        c1 = 0
        c2 = 0
        c3 = 0

        # Calculate Euclidean Distance for Train Data and sort
        eucD = np.empty((n,),dtype='f32,i4')
        for i in range(n):
                eucD[i][0] = np.linalg.norm(traindata[i,1:3]-invals)
                eucD[i][1] = traindata[i,0]
        eucD = np.sort(eucD)
        
	# Sum k's for closest samples
        for i in range(k):
            # Red
            if(eucD[i][1] == 1):
                c1 += 1
            # Green
            elif(eucD[i][1] == 2):
                c2 += 1
            # Blue
            elif(eucD[i][1] == 3):
                c3 += 1
        # Assign a class
        classarray = np.array([c1,c2,c3])
        return(np.argmax(classarray)+1)
 
# Function for handling connections. This will be used to create threads
def clientthread(conn,addr):
    print 'New thread created for new connection'
    # Sending message to connected client
    conn.send('Connected\n')
    # Infinite loop for every thread
    while True:
        # Receive data from client
        data = conn.recv(1024)
        if (data == 'exit'):
            break
        if not data: 
            break
        
    	# Get probabilities for classes (Call KNN)
	# Assume data comes like [1,2]
	# Asuume train data was [0,1,2], where class is 0
	data_list=data.split(',')
        
        # Avoid network errors
	if (len(data_list)!=2):
            continue
        print 'Received %s' % data

        # Make NumPy "understand" the data
        try:
            data=np.array(map(float,data_list))
        except:
            print "Error"
            sys.exit()

        # Run the algorithm
        result=knn(data)
        reply = 'Classified as %s' % result
        print '%s for %s' % (reply,addr)

        # Turn on and off an LED for every request successfully handled
        turnOn(1)
        conn.sendall(reply)
        turnOff(1)

    conn.close()

# Create socket
HOST = ''
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print "Socket bind complete"

# Start listening on socket, handle at most (10) connections
s.listen(10)
print 'Socket now listening'

# Create class object and train the algorithm
print("Reading Training Values")
knn_net = train("/home/root/train", k)
print("KNN Ready")


# Loop
while True:
    # Start a new thread for every new connection
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    start_new_thread(clientthread ,(conn,addr))
s.close()
