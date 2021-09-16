import numpy as np
import socket
import time
import sys
import RPi.GPIO as gpio

HOST = '127.0.0.1'  # The server's IP address
PORT = 65432  # The port used by the server

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
hallpin = 4
gpio.setup(hallpin, gpio.IN)

def sensorData():  #Sensor data simulation
    print(gpio.input(hallpin))
    return (gpio.input(hallpin))

def my_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print("Connection to server successful \nWaiting for commands...")

    while True:
        data = s.recv(1024).decode('utf-8')  #Waiting for "data"
                                             #or "quit"
        if str(data).lower() == "data":
            data = str(sensorData()).encode('utf-8')  #Sensor data simulation

            s.sendall(data)  #Sending the byte stream

            hall = s.recv(1024).decode('utf-8')#Receiving the 
            print("Controlled sensor reading: "+ hall)

        elif str(data).lower() == "quit":
            print("Shutting down client...")
            time.sleep(1)
            sys.exit()

        if not data:
            break
        else:
            pass

if __name__ == "__main__":
    while 1:
        my_client()
