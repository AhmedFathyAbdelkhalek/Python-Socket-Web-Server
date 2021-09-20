How to execute the code

Note: Client.py works with all server codes aside from sensor server. sensorClient.py is for sensorServer.py

For single connection & multithreading server:
1) Change the HOST variable to the IP address of the machine hosting the server in the server code.
2) Run server code from cmd using python servername.py 
3) Change the HOST variable to the IP address of the machine hosting the server in Client.py
4) Run Client.py in cmd
5) Input commands in server. Available commands are 'data' and 'quit'

For Flask, tunneled and sensor web server:
1) Change the HOST variable to the IP address of the machine hosting the server in the server code.
2) Run server code from cmd using python servername.py 
3) Open the URL generated
4) Click "Initialize Server"
5) Change the HOST variable to the IP address of the machine hosting the server in appropriate client code
6) Run client code in cmd
7) Input commands in server. Available commands are 'data' and 'quit'
8) Click "View Data" on the webpage
