#!C:/Users/rafaelCCI/.conda/envs/env-01
#################################################################
# File        : script_01.py
# Version     : 1.0
# Author      : camachodejay
# Date        : 2023-03-30
# Institution : Centre for Cellular Imaging, Gothenburg University
#
# Script designed as an example of calling external python scripts with
# different conda environments. This script is the 'slave' of script_2
# who calls upon it on its main
###################################################################
import skimage as sk


if __name__ == "__main__":
    print('start of script_01 main')
    print(f'skimage version: {sk.__version__}')
    print('end of script_01 main')