# test-server.py
# The server will run a python script upon request form client.
#################################################################
# File        : test-server.py
# Version     : 1.0
# Author      : camachodejay
# Date        : 2023-03-31
# Institution : Centre for Cellular Imaging, Gothenburg University
#
# Script designed as an example of calling external python scripts 
# that sit on a external server. Therefore we use TCP sockets to communicate
# the server then runs a script with a particularconda environments. 
# This script is the server that sits on the external server runing 
# Python 3.9
###################################################################
import socket
import subprocess
from os import path

local_hots = "127.0.0.1"
all_inter = "0.0.0.0"
HOST = all_inter  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break

            # converting
            output = str(data, 'UTF-8')

            if output.endswith('.py') and path.isfile(output):
                print('Now calling ' + output)
                subprocess.call(output, shell=True)
            else:
                break
            
            conn.sendall(data)