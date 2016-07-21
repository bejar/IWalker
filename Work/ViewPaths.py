"""
.. module:: ViewPaths

ViewPaths
*************

:Description: ViewPaths

    

:Authors: bejar
    

:Version: 

:Created on: 21/07/2016 11:57 

"""

__author__ = 'bejar'



from Config.Constants import odatapath, datasets, datasets2, datasets3
import os
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
import numpy as np
from Util.Trajectory import

__author__ = 'bejar'

if __name__ == '__main__':

    ldur = []
    for ds in datasets:
        lfiles = sorted(os.listdir(odatapath+ds))

        for fl in lfiles:
            pass
