#!c:/Users/rafaelCCI/.conda/envs/env-02/python
#################################################################
# File        : script_02.py
# Version     : 1.0
# Author      : camachodejay
# Date        : 2023-03-30
# Institution : Centre for Cellular Imaging, Gothenburg University
#
# Script designed as an example of calling external python scripts with
# different conda environments. This script is the 'master' of script_1
# who calls upon it on its main
###################################################################
import pandas as pd
import paquo as qp
import subprocess


if __name__ == "__main__":
    print('start of script_02 main')
    print(f'pandas version: {pd.__version__}')
    print(f'paquo version: {qp.__version__}')

    print('Now calling script 01')
    
    subprocess.call(" script_01.py", shell=True)

    print('end of script_02 main')