# -*- coding: utf-8 -*-
"""
last change: 13.11.2025
Author(s): Christoph Maier

This file contains plotting functions for S-Parameters
"""

# import needed packages
import matplotlib.pyplot as plt
import numpy as np 



'''
    This function takes S-Parameter set, which can be any number of ports, and 
    plots it. Single plots are possible, as well as subplots. Different flags 
    control title and axis names, as well as legend names. Plots can be saved
    as .png if desired.
    
    Input Parameters:
        f: frequency vector
        SParams: dict in form {'S11':Numpy array, 'S12':Numpy array,...}
        NumPorts: gives the number of ports of the S-Parameters
        how: 'allinone' for a single plot (multiple lines)
             'subplot' for subplots (one subplot for every line)
        spacing: 'lin' for linear frequency grid
                 'log' for logarithmic frequency grid
        valuetype: 'lin' for linear y-axis values
                   'dB' for y-axis values in dB
        title: string containing the overall title
        xlabel: string containing the x-axis labeling
        ylabel: string containing the y-axis labeling
        legend: 'legoff' to switch off legend
                'legon' to switch on legend. Name of the legend entries is 
                extracted from SParams
        legpos: controls position of the legend (passed through to plt.legend())
        save: 'on' plot is saved as .png
              'off' plot is not saved
        savename: string containing the name of the .png
        
    Output Parameters:
        None
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
    