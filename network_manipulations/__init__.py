# -*- coding: utf-8 -*-
"""
last change: 16.06.2026
Author(s): Christoph Maier

network_manipulations
=====================

Used for different network manipulations.

This package bundles together:
- extracting S and MM parameters out of network objects
- slice S-Parameters
- calculate MM parameters out of S parameters
- calulate the NMSE of two networks
- calculate impedance out of S-parameters (one-port, series-thru, shunt-thru)
- div. plotting functions

Intended usage:
    import network_manipulations as netman

    netman.extract_Sparam(...)
    netman.plot_impedance(...)
"""

from .myclasses import MixedModeParameter
from .osci_scripts import read_csv_1trace, mul_measurements_1ch, time_normalizer, multiplot
from .plot_functions import conv_plot_values, plot_values, plot_Sparam, plot_comp_Sparam, plot_impedance
from .SParams import extract_Sparam, extract_MMparam, slice_Sparam, S_to_MM, calc_Sparam_NMSE, calc_imp_oneport, calc_imp_seriesthru, calc_imp_shuntthru

# __all__ is optional
# Define package’s public API and control what gets imported
# when someone uses: from network_manipulations import *
__all__ = ["MixedModeParameter",
           "read_csv_1trace",
           "mul_measurements_1ch",
           "time_normalizer",
           "multiplot",
           "conv_plot_values",
           "plot_values",
           "plot_Sparam",
           "plot_comp_Sparam",
           "plot_impedance",
           "extract_Sparam",
           "extract_MMparam",
           "slice_Sparam",
           "S_to_MM",
           "calc_Sparam_NMSE",
           "calc_imp_oneport",
           "calc_imp_seriesthru",
           "calc_imp_shuntthru"]
