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
from Util.Trajectory import Trajectory
from Util.User import User
from Util.Smoothing import ALS_smoothing, numpy_smoothing

windows=['flat', 'hanning', 'hamming', 'bartlett', 'blackman']

__author__ = 'bejar'

if __name__ == '__main__':

    ldur = []
    for ds in datasets:
        lfiles = sorted(os.listdir(odatapath+ds))
        lfiles = [f.split('.')[0] for f in lfiles if f.split('.')[1] == 'usr']

        for fl in lfiles:
            frame = pd.read_csv(odatapath+ds+fl+'.csv', sep=',')
            user = User(odatapath+ds+fl)

            print (user.get_attr('User ID'))

            trajec = Trajectory(np.array(frame.loc[:, ['epx','epy']]), user.get_attr('User ID') + ' ' + str(user.get_attr('Unix Time')))
            #trajec.plot_trajectory(show=True)

            trajec.plot_over_trajectory([frame['lhfz']-frame['rhfz'], numpy_smoothing(frame['lhfz']-frame['rhfz'], window_len=5, window='blackman'),
                                         numpy_smoothing(frame['lhfz']-frame['rhfz'], window_len=5, window='hamming'),
                                         ALS_smoothing(frame['lhfz']-frame['rhfz'], 1, 0.5, niter=50)])


