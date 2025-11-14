# -*- coding: utf-8 -*-
"""
last change: 14.11.2025
Author(s): Christoph Maier

This file contains different functions for the manipulation of S parameters,
as well as the calculation of S parameters out of network files. Also
calculation and manipulation of Mixed-Mode parameters are included.

Implemented functions:
    extract_Sparam: extracts the S-parameters out of a network object
    extract_MMparam: extracts the MM-parameters out of a network object
    slice_Sparam: 'slice' dict object. Needed to extract explicit S-parameter
    S_to_MM: calculate Mixed-Mode parameters out of S-parameter
    calc_Sparam_NMSE: calculate the normalized mean-square error of two S-parameter sets
"""

# needed packages
import skrf as rf
import numpy as np

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
    f = InputNetwork.f
    fLen = len(InputNetwork.f)
    
    print('The network has ' + str(NumPorts) + ' ports.')
    
    SParams = {}
    for row in range(NumPorts):
        for column in range(NumPorts):
            key = f"S{row+1}{column+1}"
            SParams[key] = InputNetwork.s[:, row, column]

    return [NumPorts, fLen, f, SParams]



'''
    This function takes a network object and extracts the important parameters
    out of it.
    
    Input Parameters:
        InputNetwork: network object of interst
        
    Output Parameters:
        NumPorts: number of ports
        fLen: number of measured points
        f: frequency vector
        SParams: MM-Parameters, can be accessed by keyword(e.g. SParams['S11'])
'''
def extract_MMparam(InputNetwork, key_order):
    # div. error checks
    if not isinstance(InputNetwork, rf.network.Network):
        raise Exception('Given object is not a network object')
        
    NumPorts = InputNetwork.number_of_ports
    f = InputNetwork.f
    fLen = len(InputNetwork.f)
    
    print('The network has ' + str(NumPorts) + ' ports.')
    
    SParams = {}
    
    # Flatten the 2D S-matrix into a 1D list to map to your keys
    flat_s = InputNetwork.s.reshape(InputNetwork.s.shape[0], -1)

    if flat_s.shape[1] != len(key_order):
        raise Exception(f"Number of keys ({len(key_order)}) does not match number of S-parameters ({flat_s.shape[1]})")

    for idx, key in enumerate(key_order):
        SParams[key] = flat_s[:, idx]

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
def slice_Sparam(keys_to_extract, dict_input):
    dict_output = {k: dict_input[k] for k in keys_to_extract}
    
    return dict_output



'''
    This function is needed to calculate the Mixed-Mode S-Parameters out of 
    the "normal" S-Parameters dict.
    
    Input Parameters:
        dict_in: 4-port S-parameter dict
    
    Output parameters:
        dict_out: converted MM-parameter dict
'''
def S_to_MM(dict_in):
    
    S_mat = np.array([[dict_in["S11"], dict_in["S12"], dict_in["S13"], dict_in["S14"]],
                      [dict_in["S21"], dict_in["S22"], dict_in["S23"], dict_in["S24"]],
                      [dict_in["S31"], dict_in["S32"], dict_in["S33"], dict_in["S34"]],
                      [dict_in["S41"], dict_in["S42"], dict_in["S43"], dict_in["S44"]]])
    
    # Mixed-mode transform matrix
    Transform = (1/np.sqrt(2)) * np.array([[1, -1, 0, 0], [1,  1, 0, 0],
                                           [0,  0, 1, -1], [0,  0, 1,  1]])
    
    # calculate inverse of transfomr matrix
    Transform_inv = np.linalg.inv(Transform)
    
    # Apply mixed-mode transform
    # S_mm = T * S * Tinv
    S_mat_exp = S_mat.transpose(2,0,1)
    MixedMode_exp = Transform @ S_mat_exp @ Transform_inv
    MixedMode = MixedMode_exp.transpose(1,2,0)
    
    labels = ["dd", "dc", "cd", "cc"]
    dict_out = {}
    
    for i in range(4):
        for j in range(4):
            key = f"S{labels[i]}{labels[j]}"
            dict_out[key] = MixedMode[i, j, :]
    
    return dict_out



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


