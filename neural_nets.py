#!/usr/bin/python

######################################################
#  ****************************************
#  Neural Network Color Classification    \
#  Using Yocto & Numpy                    /
#  Neural Networks Classes                \
#                                         /
#  Alejandro Enedino Hernandez Samaniego  \
#  alejandro.hernandez@linux.intel.com    /
#  alejandro.hernandez@intel.com          \
#  aehs29@ieee.org                        /
#  ****************************************
######################################################

# Classes
# Red = 1
# Green = 2
# Blue = 3
# Black / Nothing = 4

# Imports
from math import *
import numpy as np
from StringIO import StringIO
import random

class knnn:
    # Constructor
    def __init__(self, trainfile, k):

        # Read Input Files (Training) and assign variables
        trainstr = open(trainfile, "r").read()
        self.traindata = np.genfromtxt(StringIO(trainstr), delimiter = ",")
        self.n = self.traindata.shape[0]
        self.k = k

    def classify(self,value):

        reds = 0
        greens = 0
        blues = 0
        blacks = 0

        n = self.n

        # Calculate Euclidean Distance for Train Data and sort
        eucD = np.empty((n,),dtype='f32,i4')
        for i in range(n):
            eucD[i][0] = np.linalg.norm(self.traindata[i,0]-value)
            eucD[i][1] = self.traindata[i,1]
        eucD = np.sort(eucD)

        # Sum k's for closest samples
        for i in range(self.k):
            # Red
            if(eucD[i][1] == 1):
                reds += 1
            # Green
            elif(eucD[i][1] == 2):
                greens += 1
            # Blue
            elif(eucD[i][1] == 3):
                blues += 1
            # Black / Nothing
            elif(eucD[i][1] == 4):
                blacks += 1

        # Assign a class
        classarray = np.array([reds,greens,blues,blacks])
        return(np.argmax(classarray)+1)


class perceptron:
    def __init__(self, trainfile, eta = 0.5, threshold = 0):

        # Read Input Files (Training) and assign variables
        trainstr = open(trainfile, "r").read()
        self.traindata = np.genfromtxt(StringIO(trainstr), delimiter = ",")
        self.eta = eta
        self.thres = threshold
        self.rmse = 0
        self.n = traindata.shape[0]

        # Declare & Initialize Weights
        self.numw = traindata.shape[1] + 1
        self.w = np.random.rand(self.numw)

        # Randomize Data
        np.random.shuffle(self.traindata)

        # Train Network
        self.train(self.traindata)

    def epoch(self):

        sse = 0
        for i in range(self.n):
            # Green is food
            if(self.traindata[i][0] == 3):
                desired = 1
            else:
                desired = -1

            output = self.output(self.traindata[i])
            error = desired - output
            self.adjust_weights(error,traindata[i])
            sse += math.pow(error,2)
            rmse = math.sqrt(sse/self.n)

    def output(self, measurement):

        v = 0

        # Multiply Input by Weight
        for i in range(self.numw - 1):
            v += self.w[i]*measurement[i+1]
        # Bias
        v += self.w[i+1]

        # Map output for perceptron
        if(v>0):
            return 1
        else:
            return -1

    def adjust_weights(self, error, measurement):

        for i in range(self.numw - 1):
            self.w[i] += self.eta*error*measurement[i+1]
        self.w[i+1] += self.eta*error

    def classify(self, measurement):

        # Input for train had a desired value so create a dummy one
        dummy = np.empty(self.numw) + 1
        dummy[0] = 0
        for i in range(self.numw):
            dummy[i+1] = measurement[i]
        return self.output(dummy)

    def train(self):

        rmse = self.rmse
        while (rmse > self.thres):
            rmse = self.epoch()
