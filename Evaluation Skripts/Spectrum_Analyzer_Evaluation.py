# -*- coding: utf-8 -*-
"""
author: Maier Christoph
date: 26.05.2025

LOREM IPSUM
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl5

"""
input variable: *filename
"""
def read_input(filename):
    
    data = []
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line and line[0].isdigit():
                row = [float(x) for x in line.split(';')]
                data.append(row)
     
        return np.array(data)
    
            
if __name__ =='__main__':
    # define files to evaluate
    filepath = 'Spectrum_Analyzer/'
    
    filename_1MHz = ['Noise_9kHz-1MHz.DAT',
                     'Vin_150V_no_load_9kHz-1MHz.DAT',
                     'Vin_150V_15mA_9kHz-1MHz.DAT',
                     'Vin_150V_50mA_9kHz-1MHz.DAT',
                     'Vin_150V_100mA_9kHz-1MHz.DAT',
                     'Vin_150V_200mA_9kHz-1MHz.DAT']

    filename_10MHz = ['Noise_9kHz-10MHz.DAT',
                      'Vin_150V_no_load_9kHz-10MHz.DAT',
                      'Vin_150V_15mA_9kHz-10MHz.DAT',
                      'Vin_150V_50mA_9kHz-10MHz.DAT',
                      'Vin_150V_100mA_9kHz-10MHz.DAT',
                      'Vin_150V_200mA_9kHz-10MHz.DAT']
    
    value_1MHz = []
    value_10MHz = []
     
    for file in filename_1MHz:
        value_1MHz.append(read_input(filepath + file))
        
    for file in filename_10MHz:
        value_10MHz.append(read_input(filepath + file))
    

        
    # creating plot
    fig = plt.figure()

    for cnt in range(len(value_1MHz)):
        plt.semilogx(value_1MHz[cnt][:,0], value_1MHz[cnt][:,1])
        #plt.semilogx(value_1MHz[cnt][:,0], value_1MHz[cnt][:,2])
        
    plt.title('Disturbances for 9kHz to 1MHz')
    plt.xlabel('Frequency in Hz')
    plt.ylabel('dBm')
    plt.legend(['noise','0mA','15mA','50mA','100mA','200mA'])
    plt.xlim(min(value_1MHz[0][:,0]), max(value_1MHz[0][:,0]))
    plt.grid(which='both', axis='both')
       
    plt.tight_layout()
    plt.show
    
    # creating plot
    fig = plt.figure()

    for cnt in range(len(value_10MHz)):
        plt.semilogx(value_10MHz[cnt][:,0], value_10MHz[cnt][:,1])
        #plt.semilogx(value_10MHz[cnt][:,0], value_10MHz[cnt][:,2])
        
    plt.title('Disturbances for 9kHz to 10MHz')
    plt.xlabel('Frequency in Hz')
    plt.legend(['noise','0mA','15mA','50mA','100mA','200mA'])
    plt.xlim(min(value_10MHz[0][:,0]), max(value_10MHz[0][:,0]))
    plt.grid(which='both', axis='both')
       
    plt.tight_layout()
    plt.show
    
