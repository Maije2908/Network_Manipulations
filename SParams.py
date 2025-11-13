# -*- coding: utf-8 -*-
"""
last change: 13.11.2025
Author(s): Christoph Maier

This file contains different functions for the manipulation of S parameters,
as well as the calculation of S parameters out of network files. Also
calculation and manipulation of Mixed-Mode parameters are included.
"""

# needed packages
import skrf as rf
import numpy as np 
import csv
from myclasses import MixedModeParameter

# definition of constants
eps = np.finfo(np.float64).eps # define epsilon (a very small number)


'''
    This function takes a network object and extracts the important parameters
    out of it.
    
    Input Parameters:
        InputNetwork: network object of interst
        
    Output Parameters:
        NumPorts: number of ports
        fLen: number of measured points
        f: frequency vector
        SParams: S-Parameters, can be accessed by keyword(e.g. SParams['S11'])
'''
def extract_Sparam(InputNetwork):
    # div. error checks
    if not isinstance(InputNetwork, rf.network.Network):
        raise Exception('Given object is not a network object')
        
    NumPorts = InputNetwork.number_of_ports
    fLen = len(InputNetwork.f)
    
    print('The network has ' + str(NumPorts) + ' ports.')
        
    f = InputNetwork.f
    
    SParams = {}
    for row in range(NumPorts):
        for column in range(NumPorts):
            key = f"S{row+1}{column+1}"
            SParams[key] = InputNetwork.s[:, row, column]

    return [NumPorts, fLen, f, SParams]



'''
    This function takes a dict S-parameter object and 'slices'. It is needed
    to extract specific S-parameters out of a whole object.
    
    Input Parameters:
        keys_to_extract: is a list of strings, used to specify the
                         keys (e.g. ['S11','S12'])
        dict_input: input S-parameter dict object
        
    Output Parameters:
        dict_output: sliced output S-parameter dict object
        
'''
def sliceSparam(keys_to_extract, dict_input):
    dict_output = {k: dict_input[k] for k in keys_to_extract}
    
    return dict_output



'''
    This function is needed to calculate the Mixed-Mode S-Parameters out of 
    the "normal" S-Parameters. The Rohde und Schwarz ZNA is not able to store
    the data in another format (as far as we know). The function needs a 4-port
    S-Parameter measurement, stored in a .csv file
    
    Input Parameters:
        path: Path of the .csv file   
    
    Output parameters:
        None
'''
def calc_Mixed_Mode_from_S(path):
    
    frequency = []
    Sdd11_re = []
    Sdd11_im = []
    Sdd12_re = []
    Sdd12_im = []
    Sdc11_re = []
    Sdc11_im = []
    Sdc12_re = []
    Sdc12_im = []
    Sdd21_re = []
    Sdd21_im = []
    Sdd22_re = []
    Sdd22_im = []
    Sdc21_re = []
    Sdc21_im = []
    Sdc22_re = []
    Sdc22_im = []
    Scd11_re = []
    Scd11_im = []
    Scd12_re = []
    Scd12_im = []
    Scc11_re = []
    Scc11_im = []
    Scc12_re = []
    Scc12_im = []
    Scd21_re = []
    Scd21_im = []
    Scd22_re = []
    Scd22_im = []
    Scc21_re = []
    Scc21_im = []
    Scc22_re = []
    Scc22_im = []
    
    if type(path) != str:
        raise Exception('Path is not a string')
    else:
        if path == '':
            raise Exception('Path is emty')                
    
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter = ';', quotechar='|')
        next(reader,None)
        next(reader,None)
        next(reader,None)   # skip header (3 rows)
        
        for row in reader:
            frequency.append(float(row[0]))
            Sdd11_re.append(float(row[1]))
            Sdd11_im.append(float(row[2]))
            Sdd12_re.append(float(row[3]))
            Sdd12_im.append(float(row[4])) 
            Sdc11_re.append(float(row[5])) 
            Sdc11_im.append(float(row[6])) 
            Sdc12_re.append(float(row[7]))
            Sdc12_im.append(float(row[8])) 
            Sdd21_re.append(float(row[9])) 
            Sdd21_im.append(float(row[10])) 
            Sdd22_re.append(float(row[11])) 
            Sdd22_im.append(float(row[12])) 
            Sdc21_re.append(float(row[13])) 
            Sdc21_im.append(float(row[14])) 
            Sdc22_re.append(float(row[15])) 
            Sdc22_im.append(float(row[16])) 
            Scd11_re.append(float(row[17])) 
            Scd11_im.append(float(row[18])) 
            Scd12_re.append(float(row[19])) 
            Scd12_im.append(float(row[20])) 
            Scc11_re.append(float(row[21])) 
            Scc11_im.append(float(row[22])) 
            Scc12_re.append(float(row[23])) 
            Scc12_im.append(float(row[24])) 
            Scd21_re.append(float(row[25])) 
            Scd21_im.append(float(row[26])) 
            Scd22_re.append(float(row[27])) 
            Scd22_im.append(float(row[28])) 
            Scc21_re.append(float(row[29])) 
            Scc21_im.append(float(row[30])) 
            Scc22_re.append(float(row[31])) 
            Scc22_im.append(float(row[32]))
            
    ntwk = MixedModeParameter(frequency, Sdd11_re, Sdd11_im, Sdd12_re, Sdd12_im,
                              Sdc11_re, Sdc11_im, Sdc12_re, Sdc12_im, Sdd21_re, Sdd21_im,
                              Sdd22_re, Sdd22_im, Sdc21_re, Sdc21_im, Sdc22_re, Sdc22_im,
                              Scd11_re, Scd11_im, Scd12_re, Scd12_im, Scc11_re, Scc11_im,
                              Scc12_re, Scc12_im, Scd21_re, Scd21_im, Scd22_re, Scd22_im,
                              Scc21_re, Scc21_im, Scc22_re, Scc22_im)
    
    return ntwk



'''
    This function calculates the normalized mean-square error (NMSE) of two
    S-parameter objects by comparing the transmission and the reflection
    coefficients separately.
    
    Input Parameters:
        SComp: network object of the S-parameter block which is compared to
               the reference one.
        SRef: network object used as reference. The frequency grid and the
              number of ports of the two S-parameter objects must be the same
              If this variable is left empty, a comparison to a infinitesimally
              small, perfecly matched line is made.
        valuetype: Flag indicating whether output values are in dB or linear
                   scale. If set to 'dB', output is in decibels; any other
                   value (or empty) means linear scale.
    
    Output parameters:
        NMSERef     Calculated NMSE for the reflection coefficients 
        NMSETrans   Calculated NMSE for the transmission coefficients
'''
def calc_Sparam_NMSE(SComp, SRef, valuetype=' '):
     
    # generate variables
    NMSERef =[]
    NMSETrans = []
    
    # div. error checks
    if not isinstance(SComp, rf.network.Network):
        raise Exception('Given object is not a network object')
    else:
        if not isinstance(SRef, rf.network.Network):
            CompareToUnityLine = True
        else:
            CompareToUnityLine = False
            if not (SComp.number_of_ports == SRef.number_of_ports):
               raise Exception('The number of ports of the two objects do not agree')
            if not (len(SComp.f) == len(SRef.f)):
                raise Exception('The number of measurement points does not match')
                
                
    NumPorts = SComp.number_of_ports
    RefNumer = 0
    RefDenom = 0
    TransNumer = 0
    TransDenom = 0
    
    if CompareToUnityLine:
        fLen = len(SComp.f)
        for row in range(NumPorts):
            for column in range(NumPorts):
                if row == column:
                    RefNumer = RefNumer + np.sum(np.square(np.abs(SComp.s[:, row, column])))
                else:
                    TransNumer = TransNumer + np.sum(np.square(np.abs(SComp.s[:, row, column] - 1)))
                    TransDenom = TransDenom + fLen
        NMSERef = RefNumer
        NMSETrans = TransNumer / TransDenom
    else:
        for row in range(NumPorts):
            for column in range(NumPorts):
                if row == column:
                    RefNumer = RefNumer + np.sum(np.square(np.abs(SComp.s[:, row, column] - SRef.s[:, row, column])))
                    RefDenom = RefDenom + np.sum(np.square(np.abs(SRef.s[:, row, column])))
                else:
                    TransNumer = TransNumer + np.sum(np.square(np.abs(SComp.s[:, row, column] - SRef.s[:, row, column])))
                    TransDenom = TransDenom + np.sum(np.square(np.abs(SRef.s[:, row, column])))
        NMSERef = RefNumer / RefDenom
        NMSETrans = TransNumer / TransDenom
        
    if valuetype == 'dB':
        NMSERef = 10*np.log10(np.abs(NMSERef + eps))
        NMSETrans = 10*np.log10(np.abs(NMSETrans + eps))
        print(f'S-Parameter comparison: \nreflect - NMSE: {NMSERef:3.1f}dB \ntransm. - NMSE: {NMSETrans:3.1f}dB\n')
    else:
        print(f'S-Parameter comparison: \nreflect - NMSE: {NMSERef:5.3f} \ntransm. - NMSE: {NMSETrans:5.3f}\n')          

    return NMSERef, NMSETrans
