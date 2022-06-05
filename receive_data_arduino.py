import serial
import matplotlib.pyplot as plt
import numpy as np 
import random

# material = "Melamina"
# mistura = "CB"

#file_generation = open()

plt.ion()
fig = plt.figure()

i = 0
x = []
y = []

# Communication With Python
# COM# is the port used in the communitcation, maybe you have to check what port your computer is using
ser = serial.Serial('/dev/ttyACM0',9600)
ser.flushInput()
ser.close()
ser.open()

while True:

    data  = ser.readline()
    print(data.decode())
    x.append(i)
    y.append(data.decode)
    y.append(data)

    plt.scatter(i, float(data))
    plt.scatter(i, float(data.decode()))
    i += 1
    plt.show()
    plt.pause(0.0001)