# -*- coding: utf-8 -*-
"""
last change: 17.12.2025
Author(s): Christoph Maier

This file contains plotting functions for S-Parameters.

The following functions are implemented:
    conv_plot_values: helper function to plot in dB or abs values
    plot_values: helper function to plot in lin or log frequency grid
    plot_Sparam: to plot S-parameter in one single plot or subplots
    plot_comp_Sparam: to plot comparison of S-parameter in one single plot or subplots
    plot_impedance: to plot impedances in one single plot
"""

# import needed packages
import matplotlib.pyplot as plt
import numpy as np 


'''
    Function to convert input parameters into linear or dB values
    (used for y-axis values).
    
    Input Parameters:
        values: array of input values
        valuetype: 'dB' for dB y-axis values
                   'lin' for linear y-axis values
                   Raises Error, if no valid keyword is found
                   
    Output Parameters:
        outval: converted outuput value
'''
def conv_plot_values(values,
                     valuetype):
    
    if valuetype == 'dB':
        outval = 20 * np.log10(np.abs(values))
    elif valuetype == 'lin':
        outval = np.abs(values)
    else:
        raise ValueError('No valid keyword for value type found.')
        
    return outval



'''
    Function to plot input values in logarithmic or linear frequency grid.
    
    Input Parameters:
        frequency: array of frequency values
        values: array of input values
        key: key for labels
        spacing: 'lin' for plot with linear frequency spacing
                 'log' for plot with logarithmic spacing 
                 'loglog' for plot with logarithmic x and y axis
                   Raises Error, if no valid keyword is found
                   
    Output Parameters:
        None
'''
def plot_values(ax,
                frequency,
                values,
                key,
                spacing):
    if spacing == 'log':
        ax.semilogx(frequency, values, label=key)
    elif spacing == 'lin':
        ax.plot(frequency, values, label=key)
    elif spacing == 'loglog':
        ax.loglog(frequency, values, label=key)
    else :
        raise ValueError('No valid keyword for spacing found.')        



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
        spacing: allow control of frequency grid
        valuetype: allow control of y-axis grid
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
def plot_Sparam(f,
                SParams,
                NumPorts,
                how='allinone',
                spacing='lin',
                valuetype='lin',
                title='',
                xlabel='',
                ylabel='',
                legend='legoff',
                legpos='best',
                save='off',
                savename='save.png'):
    
    ### single plot ###
    if how == 'allinone':
        fig, ax = plt.subplots()
        
        for key, values in SParams.items():
            yval = conv_plot_values(values, valuetype)
            plot_values(ax, f, yval, key, spacing)
                
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
        axes = axes.flatten()
        
        for ax, key in zip(axes, SParams.keys()):
            yval = conv_plot_values(SParams[key], valuetype)
            plot_values(ax, f, yval, key, spacing)
                
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
        raise ValueError('ERROR: No valid keyword for plot format found.')
        
    # save figure as png
    if save == 'on':
        plt.savefig(savename, dpi=600)
    
    # show plot
    plt.show()



'''
    This function takes two S-Parameter sets, which need to have the same
    number of and make a comparison plot. Single plots are possible, which just 
    throw everything in one plot, as well as a comparison subplot. Different
    flags control title and axis names, as well as legend names. Plots can be
    saved as .png if desired.
    
    Input Parameters:
        f_1: frequency vector of first set
        SParams_1: dict of first set in form
                   {'S11':Numpy array, 'S12':Numpy array,...}
        f_2: frequency vector of second set
        SParams_2: dict of second set in form
                   {'S11':Numpy array, 'S12':Numpy array,...}
        NumPorts: gives the number of ports of the S-Parameters (for both sets)
        how: 'allinone' for a single plot (multiple lines)
             'subplot' for subplots (one subplot for every line)
        spacing: allow control of frequency grid
        valuetype: allow control of y-axis grid
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
def plot_comp_Sparam(f_1,
                     SParams_1,
                     f_2,
                     SParams_2,
                     NumPorts,
                     how='allinone',
                     spacing='lin',
                     valuetype='lin',
                     title='',
                     xlabel='',
                     ylabel='',
                     legend='legoff',
                     legpos='best',
                     labels=['measurement 1','measurement 2'],
                     save='off',
                     savename='save.png'):
    
    ### single plot ###
    if how == 'allinone':
        fig, ax = plt.subplots()
        
        for key in SParams_1.keys():
            if key not in SParams_2:
                print('Key' + str(key) + 'not found in second dataset, skipping...')
        
            values_1 = SParams_1[key]
            values_2 = SParams_2[key]
            
            yval_1 = conv_plot_values(values_1, valuetype)
            yval_2 = conv_plot_values(values_2, valuetype)
            
            plot_values(ax, f_1, yval_1, key, spacing)
            plot_values(ax, f_2, yval_2, key, spacing)      
            
        # let frequency start at min and end at max
        plt.xlim(min(min(f_1), min(f_2)), max(max(f_1), max(f_2)))

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
        axes = axes.flatten()

        for ax, key in zip(axes, SParams_1.keys()):
            if key not in SParams_2:
                print('Key' + str(key) + 'not found in second dataset, skipping...')
            
            values_1 = SParams_1[key]
            values_2 = SParams_2[key]
            
            yval_1 = conv_plot_values(values_1, valuetype)
            yval_2 = conv_plot_values(values_2, valuetype)
            
            plot_values(ax, f_1, yval_1, key, spacing)
            plot_values(ax, f_2, yval_2, key, spacing)
            
            ax.set_title(str(key))
            ax.set_xlim(min(min(f_1), min(f_2)), max(max(f_1), max(f_2)))
            ax.grid(which='major')
            ax.grid(which='minor')
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            
            if legend  == 'legon':
                ax.legend(labels, loc=legpos)
        
        if title != '':
            plt.suptitle(title)
        
        plt.tight_layout()
        
        
    ### no keyword found ###
    else:
        raise ValueError('ERROR: No valid keyword for plot format found.')
        
    # save figure as png
    if save == 'on':
        plt.savefig(savename, dpi=600)
    
    # show plot
    plt.show()



'''
    This function takes a set of impedance values (could also be one) and plots 
    it. Only single plots are possible. Different flags control title and axis
    names, as well as legend names. Plots can be saved as .png if desired.
    
    Input Parameters:
        f: frequency list (vector)
        impedance: dict in form {'imp_1':Numpy array, 'imp_2':Numpy array,...}
        NumPorts: gives the number of ports of the S-Parameters
        spacing: allow control of frequency grid
        valuetype: allow control of y-axis grid
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
def plot_impedance(f,
                   impedance,
                   spacing='lin',
                   valuetype='lin',
                   title='',
                   xlabel='',
                   ylabel='',
                   legend='legoff',
                   legpos='best',
                   save='off',
                   savename='save.png'):
    
    fig, ax = plt.subplots()
    
    for (key, values), freq in zip(impedance.items(), f):
        yval = conv_plot_values(values, valuetype)
        plot_values(ax, freq, yval, key, spacing)
            
    # let frequency start at min and end at max
    plt.xlim(min(min(f_part) for f_part in f), max(max(f_part) for f_part in f))

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
        
    # save figure as png
    if save == 'on':
        plt.savefig(savename, dpi=600)
    
    # show plot
    plt.show()
    
    