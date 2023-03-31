# test-cd7-client.py written for the CD7 IronPython 2
# Client that sends python script to execute to server
#################################################################
# File        : test-cd7-client.py
# Version     : 1.0
# Author      : camachodejay
# Date        : 2023-03-31
# Institution : Centre for Cellular Imaging, Gothenburg University
#
# Script designed as an example of calling external python scripts 
# that sit on a external server. Therefore we use TCP sockets to communicate
# the server then runs a script with a particularconda environments. 
# This script is the "macro" that sits on the CD7. Thus runs IronPython
###################################################################
import socket

local_hots = "127.0.0.1" # used for testing locally
server_ip = "0.0.0.0" # TODO: place the server IP, make sure server firewall rules allow connection
HOST = server_ip  # The server's hostname or IP address
PORT = 65432  # The port used by the server


#create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to hots
s.connect((HOST, PORT))
# make sure to send the message in its totality
s.sendall(b"script_01.py")
# get message back from server
data = s.recv(1024)
# close socket
s.close()
# show info sent from server
print("Received: " + data)