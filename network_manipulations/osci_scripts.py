# -*- coding: utf-8 -*-
"""
author: Maier Christoph
date: 18.06.2025

This module is a selection of functions for the manipulation of generated
measurement data with an oscilloscope.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl5


'''
    This function reads a .csv file from a Oscilloscope measurement with one
    trace. The csv needs to be separated with a comma (','), at the moment. No
    check is present if this is not the case! The first column is the time 
    vector and the second column is the measured value.
    
    Input Parameters:
        filename    string which stores the filename (including path) of the
                    .csv file
        header_num  Gives the number of header lines. Since i do not know if 
                    every osci has only one header line, better to make it 
                    flexible
    
    Output parameters:
        time        vector (list) containing the time points
        yval        vector (list) containing the measured voltage points
'''
def read_csv_1trace(filename, header_num):
    
    data = []
    time = []
    yval = []
    
    with open(filename, 'r') as file:
        for cnt in range(header_num):
            file.readline()
        for line in file:
            row = [float(x) for x in line.split(',')]
            data.append(row)
    
    for cnt in range(len(data)):
        time.append(data[cnt][0])
        yval.append(data[cnt][1])
                            
    return [time, yval]


'''
    This function takes the filename of multiple .csv file from a 1 channel
    osci measurement, extracts the data and stores them in a matrix. It uses
    the function 'read_csv_1trace' for the extraction of data.
    
    Input Parameters:
        filename        string which stores the filename of the .csv file
        filepath        filepath for the stored data
        header_num      Gives the number of header lines. Since i do not know if 
                        every osci has only one header line, better to make it 
                        flexible
                        
    Output parameters:
        time        matrix (list) containing the time points
        yval        matrix (list) containing the measured voltage points
'''

def mul_measurements_1ch(filename, filepath, header_num):
    
    time = []
    yval = []   
    
    for file in filename:
        [time_temp, yval_temp] = read_csv_1trace(filepath + file, header_num)
        time.append(time_temp)
        yval.append(yval_temp)

    return [time, yval]


'''
    This function normalizes the time vector. Often it starts at negative time
    values (depending on the trigger). This function shift the time vector, so
    that it starts at 0s. Should also work if time vector only consists positive
    values.
    
    Input Parameters:
        time_old     Old time vector, consisting negative time
        
    Output Parameters:
        time         Shifted time vector, starting at 0s
'''
def time_normalizer(time_old):
    
    time = []
    
    min_val = np.min(time_old)
    time = time_old - min_val

    return time


'''
    This function plots multiple traces in one plot.
    
    Input Parameters:
        time       time matrix, consisting of the time data vectors
        yval       voltage matrix, consisting of the measured voltage vecotrs
        title      string consisting the title of the plot
        xlabel     string including the label of the x-axis
        ylabel     string including the label of the y-axis
        legend     vector of strings consisting of the legend
        xfit       optional argument for the left and right xlim
        
    Output Parameters:
        NONE
'''
def multiplot(time, yval, title, xlabel, ylabel, legend, xfit = None):
        
    plt.figure()

    for cnt in range(len(time)):
        plt.plot(time[cnt], yval[cnt])
        
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(legend)
    if xfit != None:
        plt.xlim(xfit)
    plt.grid(which='both', axis='both')
       
    plt.tight_layout()
    plt.show
