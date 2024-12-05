# -*- coding: utf-8 -*-
"""
last change: 05.12.2024
@author: christoph_m

This function calculates the NMSE of two S-parameter objects by comparing
the transmission and the reflection coefficients separately.

  Input Parameters:
      SComp  ... network object of the S-parameter block which is
                 compared to the reference one
      SRef   ... network object used as reference. The frequency grid
                 and the number of ports of the two S-parameter objects
                 must be the same
                 If this variable is left empty, a comparison to a
                 infinitesimally small, perfecly matched line
      ShowdB ... Show the calculated NMSE in dB (instead of its linear
                 value)
      ShowCMD ... Write the results to the command window

  Output parameters:
      NMSERef... Calculated NMSE for the reflection coefficients 
      NMSETrans... Calculated NMSE for the transmission coefficients

  needed packages:
      numpy

"""

# import needed packages
import numpy as np 
import skrf as rf

# set default values of the variables
eps = np.finfo(np.float64).eps
ShowCMD = False
ShowdB = False



def set_showCMD():
    global ShowCMD
    ShowCMD = True



def reset_showCMD():
    global ShowCMD
    ShowCMD = False
    


def set_showdB():
    global ShowdB
    ShowdB = True



def reset_showdB():
    global ShowdB
    ShowdB = False
    


def CalcSParameterNMSE(SComp, SRef):
     
    # generate variables
    NMSERef =[]
    NMSETrans = []
    
    # dif. error checks
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
                raise Exception('The number of mearuement points does not match')
                
                
    NumPorts = SComp.number_of_ports
    RefNumer = 0
    RefDenom = 0
    TransNumer = 0
    TransDenom = 0
    
    if CompareToUnityLine:
        fLen = len(SComp.f)
        for cnt_1 in range(NumPorts):
            for cnt_2 in range(NumPorts):
                if cnt_1 == cnt_2:
                    RefNumer = RefNumer + np.sum(np.square(np.abs(SComp.s[:, cnt_1, cnt_2])))
                else:
                    TransNumer = TransNumer + np.sum(np.square(np.abs(SComp.s[:, cnt_1, cnt_2] - 1)))
                    TransDenom = TransDenom + fLen
        NMSERef = RefNumer
        NMSETrans = TransNumer / TransDenom
    else:
        for cnt_1 in range(NumPorts):
            for cnt_2 in range(NumPorts):
                if cnt_1 == cnt_2:
                    RefNumer = RefNumer + np.sum(np.square(np.abs(SComp.s[:, cnt_1, cnt_2] - SRef.s[:, cnt_1, cnt_2])))
                    RefDenom = RefDenom + np.sum(np.square(np.abs(SRef.s[:, cnt_1, cnt_2])))
                else:
                    TransNumer = TransNumer + np.sum(np.square(np.abs(SComp.s[:, cnt_1, cnt_2] - SRef.s[:, cnt_1, cnt_2])))
                    TransDenom = TransDenom + np.sum(np.square(np.abs(SRef.s[:, cnt_1, cnt_2])))
        NMSERef = RefNumer / RefDenom
        NMSETrans = TransNumer / TransDenom
        
    if ShowdB:
        NMSERef = 10*np.log10(np.abs(NMSERef + eps))
        NMSETrans = 10*np.log10(np.abs(NMSETrans + eps))
        if ShowCMD:
            print(f'S-Parameter comparison: \nreflect - NMSE: {NMSERef:3.1f}dB \ntransm. - NMSE: {NMSETrans:3.1f}dB\n')
    elif ShowCMD:
        print(f'S-Parameter comparison: \nreflect - NMSE: {NMSERef:5.3f} \ntransm. - NMSE: {NMSETrans:5.3f}\n')          

    return NMSERef, NMSETrans
