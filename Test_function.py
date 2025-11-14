# -*- coding: utf-8 -*-
"""
last change: 14.11.2025
Author(s): Christoph Maier

This is the test function to show how to use the functions. 
"""

import skrf as rf
import network_manipulations as netman

if __name__ =='__main__':
        
    # define test files
    path = 'Examples/'
    
    # define test networks
    ntwk_1 = rf.Network(path + 'exam_1.s4p') # 4-port, 4001 pnt
    ntwk_2 = rf.Network(path + 'exam_2.s4p') # 4-port, 4001 pnt
    ntwk_3 = rf.Network(path + 'exam_3.s4p') # 4-port, 3995 pnt
    ntwk_4 = rf.Network(path + 'exam_4.s2p') # 2-port, 4001 pnt
    ntwk_5 = rf.Network(path + 'exam_5.s4p') # empty
    
    ###########################################################################
    ####################### Network Extraction examples #######################
    ###########################################################################
    
    ##### Extract Mixed-Mode Parameter from the network and store in dict #####
    key = ['Sdd11','Sdc11', 'Sdd12', 'Sdc12', 'Scd11', 'Scc11', 'Scd12', 'Scc12',
          'Sdd21', 'Sdc21', 'Sdd22', 'Sdc22', 'Scd21', 'Scc21', 'Scd22', 'Scc22']
    [number_ports_MM, number_points_MM,
     frequency_MM, MMParameter] = netman.extract_MMparam(ntwk_1, key)
    
    
    ########## Extract S-Parameter from the network and store in dict #########
    [number_ports_S, number_points_S,
     frequency_S, SParameter] = netman.extract_Sparam(ntwk_3)
    
    
    
    ###########################################################################
    ###################### Network manipulation examples ######################
    ###########################################################################
    
    ###### Calculate normalized mean-square error of two network objects ######
    [NMSE_reflect, NMSE_transm] = netman.calc_Sparam_NMSE(
        ntwk_1, ntwk_2, valuetype = 'dB')
    
    
    
    ###########################################################################
    ############ S-Parameter and MM-Parameter manipulation examples ###########
    ########################################################################### 
    
    ############### Split up S-Parameter dict into desired ones ###############
    key = ['S11','S12']
    SParameter_parts = netman.slice_Sparam(key, SParameter)
    
    
    ######### Transform 4-Port S-Parameters into Mixed-Mode Parameters ########
    MMParameter_calc = netman.S_to_MM(SParameter)
    
    
    
    ###########################################################################
    ########################### Printing  examples ############################
    ########################################################################### 
    
    #################### print S-Parameters in single plot ####################
    netman.plot_Sparam(frequency_S, SParameter, number_ports_S, how='allinone',
                       spacing='log', valuetype='dB',
                       title='Single plot', xlabel='frequency (Hz)', ylabel='|S| dB',
                       legend='legon', legpos='best',
                       save = 'on', savename='single.png')


    ###################### print S-Parameters in subplots #####################
    netman.plot_Sparam(frequency_S, SParameter, number_ports_S, how='subplot',
                       spacing='log', valuetype='dB',
                       title='Many Subplots', xlabel='frequency (Hz)', ylabel='|S| dB',
                       legend='legon', legpos='best',
                       save='on', savename='subplot.png')    
    
    
    ###################### print comparison of two S-parameter in subplots #####################
    netman.plot_comp_Sparam(frequency_S, SParameter, frequency_S, SParameter,
                            number_ports_S, how='subplot',
                            spacing='log', valuetype='dB',
                            title='Comparison Subplots', xlabel='frequency (Hz)', ylabel='|S| dB',
                            legend='legon', legpos='best', labels=['meas 1','meas 2'],
                            save='on', savename='compplot.png')
    
    
    