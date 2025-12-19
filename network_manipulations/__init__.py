# -*- coding: utf-8 -*-
"""
last change: 18.12.2025
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

    netman.extract_Sparam(...) or netman.SParams.extract_Sparam(...)
    netman.plot_impedance(...) or netman.plot_functions.plot_impedance(...)
"""
