"""
.. module:: Embedding

Embedding
*************

:Description: Embedding

    

:Authors: bejar
    

:Version: 

:Created on: 25/10/2016 10:25 

"""

__author__ = 'bejar'

from Config.Constants import odatapath, datasets, datasets2, datasets3
import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sb
from pylab import *
import numpy as np
from Util.STFT import stft
import matplotlib.gridspec as gridspec
from Util.Smoothing import ALS_smoothing, numpy_smoothing
from scipy.signal import argrelextrema
from Util import User, Exercise, Exercises, Pacientes, Trajectory
from Util.Smoothing import ALS_smoothing, numpy_smoothing

def embedding(signal, delay=2):
    """
    Plots the delay embedding of the signals from the exercise

    :param signal:
    :param delay:
    :return:
    """

    fig = plt.figure(figsize=(20, 20))

    if delay == 2:
        emb = np.zeros((signal.shape[0] - 1, 2))

        emb[:, 0] = signal[:-1]
        emb[:, 1] = signal[1:]
        ax = fig.add_subplot(111)
        plt.plot(emb[:,0], emb[:,1], c='r')
    if delay == 3:
        emb = np.zeros((signal.shape[0] - 2, 3))

        emb[:, 0] = signal[:-2]
        emb[:, 1] = signal[1:-1]
        emb[:, 2] = signal[2:]

        ax = fig.add_subplot(111, projection='3d')
        plt.plot(emb[:,0], emb[:,1], emb[:,2], c='r')


    plt.show()
    plt.close()


def time_delay(signal, delay=[1], smooth=True):
    """
    Plots the delay embedding of the signals from the exercise

    :param signal:
    :param delay:
    :return:
    """

    if smooth:
        signal = numpy_smoothing(signal, window_len=11, window='blackman')


    fig = plt.figure(figsize=(20, 20))

    row = np.sqrt(len(delay))
    if int(row) != row:
        row = int(row) + 1
        col = int(np.sqrt(len(delay))) + 1
    else:
        row = int(row)
        col = int(row)

    for i, d in zip(range(len(delay)), delay):
        emb = np.zeros((signal.shape[0] - d, 2))

        emb[:, 0] = signal[:-d]
        emb[:, 1] = signal[d:]

        ax = fig.add_subplot(row,col,i+1)
        plt.plot(emb[:,0], emb[:,1], c='r')


    plt.show()
    plt.close()


def time_delay_signals(lsignals, lsnames, delay=1, smooth=True, traj=None):
    """
    Plots the delay embedding of the signals from the exercise

    :param signal:
    :param delay:
    :return:
    """

    if smooth:
        lsmsignals = []
        for signal in lsignals:
            signal = numpy_smoothing(signal, window_len=11, window='blackman')
            lsmsignals.append(signal)
        lsignals = lsmsignals


    fig = plt.figure(figsize=(20, 20))

    row = np.sqrt(len(lsignals))
    if int(row) != row:
        row = int(row) + 1
        col = int(np.sqrt(len(lsignals))) + 1
    else:
        row = int(row) + 1
        col = int(row)

    for i, signal, nsignal in zip(range(len(lsignals)), lsignals, lsnames):
        emb = np.zeros((signal.shape[0] - delay, 2))

        emb[:, 0] = signal[:-delay]
        emb[:, 1] = signal[delay:]

        ax = fig.add_subplot(row,col,i+1)
        plt.plot(emb[:,0], emb[:,1], c='r')
        plt.title(nsignal)

    if traj is not None:
        ax = fig.add_subplot(row,col,row*col)
        plt.plot(traj[0], traj[1], c='r')


    plt.show()
    plt.close()

if __name__ == '__main__':
    vars = ['rhfx','lhfx','rhfy','lhfy','rhfz','lhfz','rnf','lnf','rs','ls']
    # 'NOGA', 'FSL'
    p = Pacientes()
    e = Exercises()
    p.from_db(pilot='FSL')
    e.from_db(pilot='FSL')
    e.delete_patients(['FSL30'])

    for ex in e.iterator():

        print (ex.uid+ '-' + str(ex.id))
        #time_delay(ex.frame['rhfz'], delay=range(1,26))
        time_delay_signals([ex.frame[s] for s in vars], vars, delay=3, traj=(ex.frame['epx'], ex.frame['epy']))