[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

# How this example works
I recomend that you first try the echo server example. This is super simple and will work locally on a single machine. Then go to the test-server example to communicate between CD7 and image analysis server.

## How to use minimal echo-server.py and echo-client.py

This is based on the article: https://realpython.com/python-sockets/#echo-client-and-server

1) Open a terminal or command prompt, navigate to the directory that contains your scripts, ensure that you have Python 3.6 or above installed and on your path, then run the server:
```
python echo-server.py
```

2) Open another terminal window or command prompt and run the client:
```
python echo-client.py 
```
3) In the server window, you should get something like:
```
Connected by ('127.0.0.1', 51188)
```
4) In the client window, you should get something like:
```
Received b'Hello, world'
```

## How to use test-server.py, with test-cd7-client.py

### prepare script.01.py to use the desired python environment
1) install the environment 1. 
2) Note the paths of env-01 via ```conda activate xxx``` and then ```which python```. 
3) Add env-01 path to the beginning of script_01.

### Firewall rules
Make sure that the firewall rules of the image analysis server allow connections originating from the microscope (CD7).

### Get the CD7 ready
1) go to the CD7 and create a new macro
2) copy the content of ```test-cd7-client.py``` on the macro and save it

### Start the test server
1) go to the anaconda prompt, and activate a Python >=3.9 environment.
2) run ```python test-server.py```
3) notice that the terminal will be **frozen**. The server is now waiting

### Run CD7 macro
Run the CD7 macro. The CD7 should get a message back from the server which echoes the script we asked for. In this case **script_01.py**. 

The terminal in the server should look like this:

```
Connected by ('xxx.yyy.zz.aa', xxxxx)
Now calling script_01.py
start of script_01 main
skimage version: 0.19.3
end of script_01 main
```
At the same time, you should see a new text file in the path of the **test-server.py**. The text file contains a timestamp for testing purposes. 