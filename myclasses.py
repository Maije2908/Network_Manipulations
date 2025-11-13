# -*- coding: utf-8 -*-
"""
last change: 13.11.2025
Author(s): Christoph Maier

Here are the needed classes stored. Implemented classes are:
    MixedModeParameter: A class to store the mixed-mode parameter.
"""



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
