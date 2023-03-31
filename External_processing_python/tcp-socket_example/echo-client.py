# echo-client.py
# The server will simply echo whatever it receives back to the client.
import socket

local_hots = "127.0.0.1" # used for testing locally
server_ip = "127.0.0.1" # TODO: place the server IP, make sure server firewall rules allow connection
HOST = server_ip  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")