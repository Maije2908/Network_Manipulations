# -*- coding: utf-8 -*-
"""
last change: 13.11.2025
Author(s): Christoph Maier


"""

# needed packages
import skrf as rf







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