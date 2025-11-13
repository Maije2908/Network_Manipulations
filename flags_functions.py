# -*- coding: utf-8 -*-
"""
last change: 13.11.2025
Author(s): Christoph Maier

These functions are used for setting flags for a better workflow

Actual implemented flags:
    ShowCMD: A flag which controls if different values are shown in the 
             command prompt
"""

# set default values of the variables
ShowCMD = False # Flag if output in the command line should be shown


'''
    This function sets the global ShowCMD flag. The flag controls, if results
    will be shown in the command line. 
    
    Input Parameters:
        None
    
    Output parameters:
        None
'''
def set_showCMD():
    global ShowCMD
    ShowCMD = True



'''
    This function resets sets the global ShowCMD flag. The flag controls, if
    results will be shown in the command line. 
    
    Input Parameters:
        None
    
    Output parameters:
        None
'''
def reset_showCMD():
    global ShowCMD
    ShowCMD = False
    