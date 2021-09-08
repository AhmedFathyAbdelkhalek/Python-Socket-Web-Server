from _thread import *
import socket
import encodings
import sys
import time

HOST = '127.0.0.1' #Host IP Address
PORT = 65432  #Port to listen on
ThreadCount = 0 #Thread number counter
firstTime = True #Indicates whether its the first time to call my_server()
connectedClients = []

def process_data_from_client(x):  #Function to
    x1, y1 = x.split(",")  #split incoming Data
    return x1, y1
    
def threadedConnection(connection):
    global firstTime
    
    with connection:
        while True:
            myInput = input("Enter command: ")
            # If a random command is given, start over
            while (str(myInput).lower() != "data" and str(myInput).lower() != "quit"):
                myInput = input("Enter command: ")

            # Encode the message
            my_inp = myInput.encode('utf-8')

            # Send request to client
            connection.sendall(my_inp)

            # If input command is quit, terminate the connection
            if str(myInput).lower() == "quit":
                print("Terminating client connection...")
                connectedClients.pop()
                time.sleep(1)
                sys.exit()

            # Get data from client
            data = connection.recv(1024).decode('utf-8')
            data
            # Process the data (comma seperated value)
            x_temperature, y_humidity = process_data_from_client(data)

            print("Temperature {}".format(x_temperature))
            print("Humidity {}".format(y_humidity))

            # Calculating controlled values and sending them back to the client
            temperature = float(x_temperature) * 1.5
            controlledTemp = str(temperature).encode('utf-8')

            humidity = float(y_humidity) * 1.5
            controlledHumidity = str(humidity).encode('utf-8')

            connection.sendall(controlledTemp)
            connection.sendall(controlledHumidity)
            time.sleep(1)
            
def my_server():
    global firstTime
    global ThreadCount
    global connectedClients
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((HOST, PORT))
    s.listen(5)
    if firstTime:
        #Inidcating the server has started
        print("Server Started \nWaiting for clients...")
        firstTime =  False
    while True:
        conn, addr = s.accept() #Accepting connection requests
        print("Connection accepted... \nConnected to", addr)
        connectedClients.append(addr[0])
        print("Starting new thread...")
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
        start_new_thread(threadedConnection, (conn, )) #Creating a new thread
    s.close() #Closing the socket

if __name__ == "__main__":
    while 1:
        my_server()
