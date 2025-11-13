# -*- coding: utf-8 -*-
"""
last change: 13.11.2025
Author(s): Christoph Maier

This module is a selection of functions for the manipulations of S-Parameters.
"""

# import needed packages
import matplotlib.pyplot as plt
import numpy as np 
import skrf as rf
import csv

# import my functions
from flags import *

# definition of constants
eps = np.finfo(np.float64).eps # define epsilon (a very small number)


"""
    A class to represent mixed-mode S-parameters (scattering parameters) for 
    a network over a range of frequencies. Mixed-mode parameters are a special
    kind of S-parameters, calculating the response to differential-mode (DM) 
    and common-mode (CM) signals. 

    Attributes:
        frequency (list): A list of the frequency points.
        
        Differential-to-Differential S-parameters:
        - Sdd11: DM excitation @P1; DM measurement @P1
        - Sdd12: DM excitation @P1; DM measurement @P2
        - Sdd21: DM excitation @P2; DM measurement @P1
        - Sdd22: DM excitation @P2; DM measurement @P2

        Differential-to-Common S-parameters:
        - Sdc11: DM excitation @P1; CM measurement @P1
        - Sdc12: DM excitation @P1; CM measurement @P2
        - Sdc21: DM excitation @P2; CM measurement @P1
        - Sdc22: DM excitation @P2; CM measurement @P2

        Common-to-Differential S-parameters:
        - Scd11: CM excitation @P1; DM measurement @P1
        - Scd12: CM excitation @P1; DM measurement @P2
        - Scd21: CM excitation @P2; DM measurement @P1
        - Scd22: CM excitation @P2; DM measurement @P2

        Common-to-Common S-parameters:
        - Scc11: CM excitation @P1; CM measurement @P1
        - Scc12: CM excitation @P1; CM measurement @P2
        - Scc21: CM excitation @P2; CM measurement @P1
        - Scc22: CM excitation @P2; CM measurement @P2

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
        Initializes the MixedModeParameter class by combining the real and
        imaginary parts of the S-parameters into lists of complex numbers for
        each parameter.
    
        Parameters:
            frequency (list): A list of frequency points.
            sdd11_re, sdd11_im, ..., scc22_im (list): Real and imaginary parts
                                                    of the S-parameters.
    
        Each S-parameter is represented as a list of complex numbers
        corresponding to each frequency point.
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
    
    if ShowCMD:
        print('The network has ' + str(NumPorts) + ' ports.')
        
    f = InputNetwork.f
    
    SParams = {}
    for row in range(NumPorts):
        for column in range(NumPorts):
            key = f"S{row+1}{column+1}"
            SParams[key] = InputNetwork.s[:, row, column]

    return [NumPorts, fLen, f, SParams]
              


'''

'''    
def plot_Sparam(f, SParams, NumPorts, how='allinone',
                spacing='lin', valuetype='lin',
                title='', xlabel='', ylabel='',
                legend='legoff', legpos='best',
                save='off', savename='save.png'):
    
    ### single plot ###
    if how == 'allinone':
        for key, values in SParams.items():
            # check if values should be dB or not
            if valuetype == 'dB' :
                yval =  20 * np.log10(np.abs(values))
            elif valuetype == 'lin':
                yval = np.abs(values)
            else:
                print('No valid keyword for value type found.')
                return
            
            # check if spacing should be logarithmic or linear
            if spacing == 'log':
                plt.semilogx(f, yval, label=key)
            elif spacing == 'lin':
                plt.plot(f, yval, label=key)
            else :
                print('No valid keyword for spacing found.')  
                return
                
        # let frequency start at min and end at max
        plt.xlim(min(f), max(f))

        # labeling and stuff
        if xlabel != '':
            plt.xlabel(xlabel)
        
        if ylabel != '':
            plt.ylabel(ylabel)

        if title != '':
            plt.title(title)
        if legend  == 'legon':
            plt.legend(loc=legpos)
            
        plt.grid(which='major')
        plt.grid(which='minor')
        
        
    ### subplots ###
    elif how == 'subplot':
        fig, axes = plt.subplots(NumPorts, NumPorts, figsize=(4*NumPorts, 4*NumPorts))

        for row in range(NumPorts):
            for column in range(NumPorts):
                # handle 1x1 case
                ax = axes[row, column] if NumPorts > 1 else axes
                
                key = f"S{row+1}{column+1}"
                if SParams[key].size > 0:
                    # check if values should be dB or not
                    if valuetype == 'dB' :
                        yval =  20 * np.log10(np.abs(SParams[key]))
                    elif valuetype == 'lin':
                        yval = np.abs(SParams[key])
                    else:
                        print('No valid keyword for value type found.')
                        return
                    
                    # check if spacing should be logarithmic or linear
                    if spacing == 'log':
                        ax.semilogx(f, yval, label=key)
                    elif spacing == 'lin':
                        ax.plot(f, yval, label=key)
                    else :
                        print('No valid keyword for spacing found.')  
                        return
                    
                    ax.set_title(str(key))
                    ax.set_xlim(min(f), max(f))
                    ax.grid(which='major')
                    ax.grid(which='minor')
                    ax.set_xlabel(xlabel)
                    ax.set_ylabel(ylabel)
            
        plt.suptitle(title)
        plt.tight_layout()
        
        
    ### no keyword found ###
    else:
        print('ERROR: No valid keyword for plot format found.')
        
    # save figure as png
    if save == 'on':
        plt.savefig(savename, dpi=600)
    
    # show plot
    plt.show()

    
    
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
        if ShowCMD:
            print(f'S-Parameter comparison: \nreflect - NMSE: {NMSERef:3.1f}dB \ntransm. - NMSE: {NMSETrans:3.1f}dB\n')
    elif ShowCMD:
        print(f'S-Parameter comparison: \nreflect - NMSE: {NMSERef:5.3f} \ntransm. - NMSE: {NMSETrans:5.3f}\n')          

    return NMSERef, NMSETrans



'''
    This function is needed to calculate the Mixed-Mode S-Parameters out of 
    the "normal" S-Parameters. The Rohde und Schwarz ZNA is not able to store
    the data in another format (as far as we know). The function needs a 4-port
    S-Parameter measurement, stored in a .csv file
    
    Input Parameters:
        path   Path of the .csv file   
    
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











