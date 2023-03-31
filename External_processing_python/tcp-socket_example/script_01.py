#!c:/Users/rafaelCCI/.conda/envs/env-01/python
# slave script to test/server.py
#################################################################
# File        : script_01.py
# Version     : 1.0
# Author      : camachodejay
# Date        : 2023-03-30
# Institution : Centre for Cellular Imaging, Gothenburg University
#
# Script designed as an example of calling external python scripts with
# different conda environments. This script is the 'slave' of test-server.py
# The script checks connection to proper conda environment by importing
# skimage and then creates a .txt with date/time for testing
###################################################################
import skimage as sk
import datetime

def GetDateTimeString():
    """ Get the current date and time in a formatted string
    """
    dt = datetime.datetime.now()
    strDateTimeCurrent = dt.strftime('%Y-%m-%d_%H:%M:%S')
    return strDateTimeCurrent


if __name__ == "__main__":
    print('start of script_01 main')
    print(f'skimage version: {sk.__version__}')
    print('end of script_01 main')

    
    with open('outuput_s1.txt', 'w') as f:
        f.write('Created a new text file!\n')
        f.write('At date-time: ' + GetDateTimeString())