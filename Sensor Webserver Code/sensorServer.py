from flask import Flask, render_template
from _thread import *
import socket
import encodings
import sys
import time
import os
import threading

HOST = '127.0.0.1' #Host IP Address
PORT = 65432  #Port to listen on
ThreadCount = 0 #Thread number counter
firstTime = True #Indicates whether its the first time to call my_server()
connectedClients = []
data = None
data_view = """"""

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/init')
def init():
    my_server()

@app.route('/data')
def data():
    global data_view
    return f"""<html><head><META HTTP-EQUIV="refresh"
           CONTENT="1"></head><body>"""+ data_view +"""</body></html>"""

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
def threadedConnection(connection):
    global firstTime
    global data_view
    
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

            print("Hall Effect {}".format(data))

            #Calculating controlled value and sending it back to the server
            hall = int(data)
            controlledHall = hall*1.3
            encodedHall = str(controlledHall).encode('utf-8')
            
            data_view =f'''<p>Sensor Reading: {data} <br/>Controlled Value
            : {controlledHall} <br/><br/></p>'''+data_view

            connection.sendall(encodedHall)
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
        firstTime = False
    while True:
        conn, addr = s.accept() #Accepting connection requests
        print("Connection accepted... \nConnected to", addr)
        connectedClients.append(addr[0])
        print("Starting new thread...")
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
        start_new_thread(threadedConnection, (conn, )) #Creating a new thread
    s.close() #Closing the socket

def url():
    os.system('cmd /k "lt --port 5000"')

if __name__ == '__main__':
    #threading.Thread(target=url).start()
    app.run(debug=False, host='0.0.0.0') #Building the Flask app
