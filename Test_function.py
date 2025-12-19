# -*- coding: utf-8 -*-
"""
last change: 17.12.2025
Author(s): Christoph Maier

This is the test function to show how to use the functions. 
"""

import skrf as rf
import network_manipulations as netman

if __name__ =='__main__':

    ###########################################################################
    ########################### Define test network ###########################
    ###########################################################################    

    path_ntwk = 'Examples/Touchstone/'
    
    ntwk_1 = rf.Network(path_ntwk + 'exam_1.s4p') # 4-port, 4001 pnt
    ntwk_2 = rf.Network(path_ntwk + 'exam_2.s4p') # 4-port, 4001 pnt
    ntwk_3 = rf.Network(path_ntwk + 'exam_3.s4p') # 4-port, 3995 pnt
    ntwk_4 = rf.Network(path_ntwk + 'exam_4.s2p') # 2-port, 4001 pnt
    ntwk_5 = rf.Network(path_ntwk + 'exam_5.s4p') # empty
    ntwk_6 = rf.Network(path_ntwk + 'exam_6.s1p') # 1-port, 501 pnt
    
    
    ###########################################################################
    ############### Define test files for Osci (.csv) evaluation ##############
    ###########################################################################   
    
    path_osci = 'Examples/Osci/'
    
    osci_exam_1 = path_osci + 'exam_1.csv'
    

    ###########################################################################
    ####################### Network Extraction examples #######################
    ###########################################################################
    
    ##### Extract Mixed-Mode Parameter from the network and store in dict #####
    key = ['Sdd11','Sdc11', 'Sdd12', 'Sdc12', 'Scd11', 'Scc11', 'Scd12', 'Scc12',
          'Sdd21', 'Sdc21', 'Sdd22', 'Sdc22', 'Scd21', 'Scc21', 'Scd22', 'Scc22']
    [number_ports_MM, number_points_MM,
     frequency_MM, MMParameter] = netman.extract_MMparam(ntwk_1, key)

    
    ########## Extract S-Parameter from the network and store in dict #########
    # 2-port
    [number_ports_S,
     number_points_S,
     frequency_S,
     SParameter] = netman.extract_Sparam(ntwk_3)
    
    # 1 port
    [number_ports_S_one,
     number_points_S_one,
     frequency_S_one,
     SParameter_one] = netman.extract_Sparam(ntwk_6)    
    
    ###########################################################################
    ###################### Network manipulation examples ######################
    ###########################################################################
    
    ###### Calculate normalized mean-square error of two network objects ######
    [NMSE_reflect,
     NMSE_transm] = netman.calc_Sparam_NMSE(ntwk_1,
                                            ntwk_2,
                                            valuetype = 'dB')
    
    
    ###########################################################################
    ############ S-Parameter and MM-Parameter manipulation examples ###########
    ###########################################################################
    
    ############### Split up S-Parameter dict into desired ones ###############
    key = ['S11','S12']
    SParameter_parts = netman.slice_Sparam(key,
                                           SParameter)
    
    ######### Transform 4-Port S-Parameters into Mixed-Mode Parameters ########
    MMParameter_calc = netman.S_to_MM(SParameter)
    
    
    ###########################################################################
    ###################### Impedance calulation examples ######################
    ###########################################################################
    # S-Parameters are arbitrary. Impedance values are nonsense
    key = 'imp_one'
    impedance_one = netman.calc_imp_oneport(frequency_S_one,
                                            SParameter_one['S11'],
                                            key)

    key = 'imp_series'
    impedance_series = netman.calc_imp_seriesthru(frequency_S,
                                                   SParameter['S21'],
                                                   key)
    
    key = 'imp_shunt'
    impedance_shunt = netman.calc_imp_shuntthru(frequency_S,
                                                SParameter['S21'],
                                                key)
    
    
    
    
    
    
    ###########################################################################
    ################# Oscilloscope (.csv) evaluation examples #################
    ###########################################################################
    
    filename = 'Testdata/TESTDATA.csv'
    [a,b] = netman.read_csv_1trace(filename, 1) 







    
    
    
    ###########################################################################
    ########################### Printing  examples ############################
    ########################################################################### 
    
    #################### print S-Parameters in single plot ####################
    netman.plot_Sparam(frequency_S,
                       SParameter,
                       number_ports_S,
                       how='allinone',
                       spacing='log',
                       valuetype='dB',
                       title='Single plot',
                       xlabel='frequency (Hz)',
                       ylabel='|S| (dB)',
                       legend='legon',
                       legpos='best',
                       save = 'on',
                       savename='single.png')

    ###################### print S-Parameters in subplots #####################
    netman.plot_Sparam(frequency_S,
                       SParameter,
                       number_ports_S,
                       how='subplot',
                       spacing='log',
                       valuetype='dB',
                       title='Many Subplots',
                       xlabel='frequency (Hz)',
                       ylabel='|S| (dB)',
                       legend='legon',
                       legpos='best',
                       save='on',
                       savename='subplot.png')    
    
    ############# print comparison of two S-parameter in subplots #############
    netman.plot_comp_Sparam(frequency_S,
                            SParameter,
                            frequency_S,
                            SParameter,
                            number_ports_S,
                            how='subplot',
                            spacing='log',
                            valuetype='dB',
                            title='Comparison Subplots',
                            xlabel='frequency (Hz)',
                            ylabel='|S| (dB)',
                            legend='legon',
                            legpos='best',
                            labels=['meas 1','meas 2'],
                            save='on',
                            savename='compplot.png')

    ### print impedances in one plot + valid way to build dict out multiple ###
    freq_test = [frequency_S_one, frequency_S, frequency_S]
    imp_test = {**impedance_one, **impedance_series, **impedance_shunt}
    
    netman.plot_impedance(freq_test,
                          imp_test,
                          spacing='loglog',
                          valuetype='lin',
                          title='Comparison Impedance',
                          xlabel='frequency (Hz)',
                          ylabel='|Z| (Ohm)',
                          legend='legon',
                          legpos='best',
                          save='on',
                          savename='impedance.png')
    
    