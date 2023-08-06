"""
test1 to test multiple module package.
"""

import sys
import os
import subprocess
import matplotlib.pyplot as plt

########################################

#plots customizations; see https://matplotlib.org/3.2.1/tutorials/introductory/customizing.html

def customize_plots(labelsize = 20, ticklabelsize = 15, legendfontsize = 13, savefigdpi = 600):

    #axes
    mpl.rcParams['axes.linewidth'] = 2.0
    mpl.rcParams['axes.labelsize'] = labelsize
    mpl.rcParams['font.family'] = 'Arial'

    #ticks
    mpl.rcParams['xtick.labelsize'] = ticklabelsize
    mpl.rcParams['ytick.labelsize'] = ticklabelsize

    mpl.rcParams['xtick.major.size'] = 6.0
    mpl.rcParams['xtick.major.width'] = 2.0
    mpl.rcParams['xtick.minor.size'] = 6.0
    mpl.rcParams['xtick.minor.width'] = 2.0

    mpl.rcParams['ytick.major.size'] = 6.0
    mpl.rcParams['ytick.major.width'] = 2.0
    mpl.rcParams['ytick.minor.size'] = 6.0
    mpl.rcParams['ytick.minor.width'] = 2.0

    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'

    mpl.rcParams['xtick.major.pad'] = 5.0
    mpl.rcParams['xtick.minor.pad'] = 5.0

    #legend
    mpl.rcParams['patch.linewidth'] = 2.0
    mpl.rcParams['legend.fontsize'] = legendfontsize
    mpl.rcParams['legend.edgecolor'] = 'black'
    mpl.rcParams['legend.title_fontsize'] = 15
    mpl.rcParams['legend.labelspacing'] = 0.1
    mpl.rcParams['legend.borderpad'] = 0.3

    #math type
    mpl.rcParams['mathtext.default'] = 'regular'

    mpl.rcParams['savefig.dpi'] = savefigdpi
    mpl.rcParams['savefig.bbox'] = 'tight'

###############################################################################################################################

b = 10
