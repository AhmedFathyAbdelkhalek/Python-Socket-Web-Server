import numpy as np
import socket
import time
import sys

HOST = '127.0.0.1'  # The server's IP address
PORT = 65432  # The port used by the server

def random_data():  #Sensor data simulator
    x1 = np.random.randint(0, 65, None)  #Simulated temperature
    y1 = np.random.randint(0, 55, None)  #Simulated humidity
    my_sensor = "{},{}".format(x1, y1)
    return my_sensor  #Return data separated by commas

def my_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print("Connection to server successful \nWaiting for commands...")

    while True:
        data = s.recv(1024).decode('utf-8')  #Waiting for "data"
                                             #or "quit"
        if str(data).lower() == "data":
            data = random_data().encode('utf-8')  #Sensor data simulation

            s.sendall(data)  #Sending the byte stream

            temp = s.recv(1024).decode('utf-8')  #Receiving the
            humidity = s.recv(1024).decode('utf-8') #controlled values
            print("Controlled temperature: " + temp)
            print("Controlled humidity: " + humidity)

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
