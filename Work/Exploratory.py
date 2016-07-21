"""
.. module:: Exploratory

Exploratory
*************

:Description: Exploratory

    

:Authors: bejar
    

:Version: 

:Created on: 21/07/2016 10:17 

"""


from Config.Constants import odatapath, datasets, datasets2, datasets3
import os
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
import numpy as np


__author__ = 'bejar'

if __name__ == '__main__':

    ldur = []
    for ds in datasets:
        lfiles = sorted(os.listdir(odatapath+ds))

        for fl in lfiles:

            frame = pd.read_csv(odatapath+ds+fl, sep=',')
            ldur.append(len(frame)*0.04)
    frame = pd.DataFrame(ldur)

    print(frame.describe())

    fig = plt.figure()
    fig.set_figwidth(6)
    fig.set_figheight(4)

    ax = fig.add_subplot(1, 1, 1)
    sn.distplot(ldur, norm_hist=True, bins=50)

    plt.show()
