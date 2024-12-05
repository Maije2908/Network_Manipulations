# -*- coding: utf-8 -*-
"""
last change: 05.12.2024
@author: Christoph Maier

This module is a selection of functions for manipulations of S-Parameters.
"""

# import needed packages
import numpy as np 
import skrf as rf

# set default values of the variables
eps = np.finfo(np.float64).eps # define epsilon (a very small number)
ShowCMD = False # Flag if output in the command line should be shown
ShowdB = False # Flag if results should be given in dB


"""
    A class to represent mixed-mode S-parameters (scattering parameters) for 
    a network over a range of frequencies.

    Attributes:
        frequency (list): A list of the frequency points.
        
        Differential-to-Differential S-parameters:
        - Sdd11: Input reflection coefficient for differential signals.
        - Sdd12: Reverse transmission coefficient for differential signals.
        - Sdd21: Forward transmission coefficient for differential signals.
        - Sdd22: Output reflection coefficient for differential signals.

        Differential-to-Common S-parameters:
        - Sdc11: Reflection coefficient from differential to common-mode at input.
        - Sdc12: Reverse transmission coefficient from differential to common-mode.
        - Sdc21: Forward transmission coefficient from differential to common-mode.
        - Sdc22: Reflection coefficient from differential to common-mode at output.

        Common-to-Differential S-parameters:
        - Scd11: Reflection coefficient from common-mode to differential at input.
        - Scd12: Reverse transmission coefficient from common-mode to differential.
        - Scd21: Forward transmission coefficient from common-mode to differential.
        - Scd22: Reflection coefficient from common-mode to differential at output.

        Common-to-Common S-parameters:
        - Scc11: Input reflection coefficient for common-mode signals.
        - Scc12: Reverse transmission coefficient for common-mode signals.
        - Scc21: Forward transmission coefficient for common-mode signals.
        - Scc22: Output reflection coefficient for common-mode signals.

    Methods:
        None
"""
class MixedModeParameter:
    def __init__(self, frequency, sdd11_re, sdd11_im, sdd12_re, sdd12_im,
                 sdc11_re, sdc11_im, sdc12_re, sdc12_im, sdd21_re, sdd21_im,
                 sdd22_re, sdd22_im, sdc21_re, sdc21_im, sdc22_re, sdc22_im,
                 scd11_re, scd11_im, scd12_re, scd12_im, scc11_re, scc11_im,
                 scc12_re, scc12_im, scd21_re, scd21_im, scd22_re, scd22_im,
                 scc21_re, scc21_im, scc22_re, scc22_im):
        
        """
        Initializes the MixedModeParameter class by combining the real and imaginary
        parts of the S-parameters into lists of complex numbers for each parameter.
    
        Parameters:
            frequency (list): A list of frequency points.
            sdd11_re, sdd11_im, ..., scc22_im (list): Real and imaginary parts of the S-parameters.
    
        Each S-parameter is represented as a list of complex numbers corresponding
        to each frequency point.
        """
        self.frequency = frequency
        self.Sdd11 = [complex(r,i) for r, i in zip(sdd11_re, sdd11_im)]
        self.Sdd12 = [complex(r,i) for r, i in zip(sdd12_re, sdd12_im)]
        self.Sdc11 = [complex(r,i) for r, i in zip(sdc11_re, sdc11_im)]
        self.Sdc12 = [complex(r,i) for r, i in zip(sdc12_re, sdc12_im)]
        self.Sdd21 = [complex(r,i) for r, i in zip(sdd21_re, sdd21_im)]
        self.Sdd22 = [complex(r,i) for r, i in zip(sdd22_re, sdd22_im)]
        self.Sdc21 = [complex(r,i) for r, i in zip(sdc21_re, sdc21_im)]
        self.Sdc22 = [complex(r,i) for r, i in zip(sdc22_re, sdc22_im)]
        self.Scd11 = [complex(r,i) for r, i in zip(scd11_re, scd11_im)]
        self.Scd12 = [complex(r,i) for r, i in zip(scd12_re, scd12_im)]
        self.Scc11 = [complex(r,i) for r, i in zip(scc11_re, scc11_im)]
        self.Scc12 = [complex(r,i) for r, i in zip(scc12_re, scc12_im)]
        self.Scd21 = [complex(r,i) for r, i in zip(scd21_re, scd21_im)]
        self.Scd22 = [complex(r,i) for r, i in zip(scd22_re, scd22_im)]
        self.Scc21 = [complex(r,i) for r, i in zip(scc21_re, scc21_im)]
        self.Scc22 = [complex(r,i) for r, i in zip(scc22_re, scc22_im)]
        
        

'''
    This function sets the global ShowCMD variable. Results will be shown in 
    the command line. 
    
    Input Parameters:
        None
    
    Output parameters:
        None
'''
def set_showCMD():
    global ShowCMD
    ShowCMD = True



'''
    This function resets sets the global ShowCMD variable. Results will be shown
    in the command line. 
    
    Input Parameters:
        None
    
    Output parameters:
        None
'''
def reset_showCMD():
    global ShowCMD
    ShowCMD = False
    


'''
    This function sets the global ShowdB variable. Results will be shown as 
    dB values. 
    
    Input Parameters:
        None
    
    Output parameters:
        None
'''
def set_showdB():
    global ShowdB
    ShowdB = True



'''
    This function resets the global ShowdB variable. Results will not be shown
    as dB values. 
    
    Input Parameters:
        None
    
    Output parameters:
        None
'''
def reset_showdB():
    global ShowdB
    ShowdB = False
   
    
   
'''
    This function calculates the normalized mean-square error (NMSE) of two
    S-parameter objects by comparing the transmission and the reflection
    coefficients separately.
    
    Input Parameters:
        SComp  ... network object of the S-parameter block which is
                   compared to the reference one
        SRef   ... network object used as reference. The frequency grid
                   and the number of ports of the two S-parameter objects
                   must be the same
                   If this variable is left empty, a comparison to a
                   infinitesimally small, perfecly matched line
    
    Output parameters:
        NMSERef... Calculated NMSE for the reflection coefficients 
        NMSETrans... Calculated NMSE for the transmission coefficients
'''
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
        
    if ShowdB:
        NMSERef = 10*np.log10(np.abs(NMSERef + eps))
        NMSETrans = 10*np.log10(np.abs(NMSETrans + eps))
        if ShowCMD:
            print(f'S-Parameter comparison: \nreflect - NMSE: {NMSERef:3.1f}dB \ntransm. - NMSE: {NMSETrans:3.1f}dB\n')
    elif ShowCMD:
        print(f'S-Parameter comparison: \nreflect - NMSE: {NMSERef:5.3f} \ntransm. - NMSE: {NMSETrans:5.3f}\n')          

    return NMSERef, NMSETrans
