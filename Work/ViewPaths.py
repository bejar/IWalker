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

from Util.Smoothing import ALS_smoothing, numpy_smoothing
from Util import User, Exercise, Exercises, Pacientes, Trajectory

windows=['flat', 'hanning', 'hamming', 'bartlett', 'blackman']

__author__ = 'bejar'


def do_it_from_files():
    """

    :return:
    """
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



if __name__ == '__main__':

    #ldur = []

    p = Pacientes()
    e = Exercises()
    p.from_db(pilot='NOG')
    e.from_db(pilot='NOG')

    for ex in e.iterator():

        print (ex.uid, ex.id)

        trajec = Trajectory(np.array(ex.frame.loc[:, ['epx','epy']]), exer=ex.uid + ' ' + str(ex.id))
        # trajec.plot_trajectory(show=True)

        # trajec.plot_over_trajectory([ex.frame['lhfz']-ex.frame['rhfz'], numpy_smoothing(ex.frame['lhfz']-ex.frame['rhfz'], window_len=5, window='blackman'),
        #                              numpy_smoothing(ex.frame['lhfz']-ex.frame['rhfz'], window_len=5, window='hamming'),
        #                              ALS_smoothing(ex.frame['lhfz']-ex.frame['rhfz'], 1, 0.5, niter=50)])

        ex.classify(criteria='speed')
        trajec.plot_over_trajectory([(ex.frame['rs'] - ex.frame['ls'])*10, np.abs(ex.frame['lhfx']-ex.frame['rhfx'])])

