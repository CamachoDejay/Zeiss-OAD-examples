#!C:/Users/rafaelCCI/.conda/envs/env-02

import pandas as pd
import subprocess


if __name__ == "__main__":
    print('start of script_02 main')
    print(f'pandas version: {pd.__version__}')

    print('Now calling script 01')
    
    subprocess.call(" python script_01.py", shell=True)

    print('end of script_02 main')