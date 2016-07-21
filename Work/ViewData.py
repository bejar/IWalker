"""
.. module:: ViewData

ViewData
*************

:Description: ViewData

    

:Authors: bejar
    

:Version: 

:Created on: 18/07/2016 14:52 

"""

__author__ = 'bejar'

from Config.Constants import odatapath, datasets, datasets2, datasets3
import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
import numpy as np
from Util.STFT import stft
import matplotlib.gridspec as gridspec
from Util.Smoothing import ALS_smoothing
from scipy.signal import argrelextrema
from Util.User import User

def total_norm(x, y, z):
    return np.sqrt(x*x+y*y+z*z)


def cosinus_angle(x1,y1,z1,x2,y2,z2):
    return((x1*x2+y1*y2+z1*z2) /(total_norm(x1,y1,z1)*total_norm(x2,y2,z2)))



def plot_forces():
    """
    Plots the forces along the trajectory and their SFFT
    :return:
    """
    fig = plt.figure(figsize=(60, 20))
    print('L=', len(frame['lhfx']))
    lensig = len(frame['lhfx'])

    if lensig < psfftl:
        sfftl = psfftl / 2
        while lensig < sfftl:
            sfftl = sfftl / 2

        sffts = psffts / 4
    else:
        sfftl = psfftl
        sffts = psffts

    ax = fig.add_subplot(331, projection='3d')
    plt.plot(frame['epx'], frame['epy'], frame['lhfx'], c='r')
    plt.plot(frame['epx'], frame['epy'], frame['rhfx'], c='b')
    ax = fig.add_subplot(332, projection='3d')
    plt.plot(frame['epx'], frame['epy'], frame['lhfy'], c='r')
    plt.plot(frame['epx'], frame['epy'], frame['rhfy'], c='b')
    ax = fig.add_subplot(333, projection='3d')
    plt.plot(frame['epx'], frame['epy'], frame['lhfz'], c='r')
    plt.plot(frame['epx'], frame['epy'], frame['rhfz'], c='b')

    # ax = fig.add_subplot(111, projection='3d')
    # plt.plot(frame['epx'], frame['epy'], frame['acc'], c='r')
    # plt.plot(frame['epx'], frame['epy'], frame['magn'], c='b')
    # plt.plot(frame['epx'], frame['epy'], frame['gyro'], c='g')

    vec = frame['lhfx']
    vec = stft(vec, sfftl, sffts, ban=ban)
    ax = fig.add_subplot(334, autoscale_on=True)
    plt.imshow(vec, cmap=plt.cm.afmhot, interpolation='lanczos', aspect='auto',
               extent=[0, freq, int((len(frame['lhfx']) - sfftl) / (sfftl / sffts)), 0])

    vec = frame['lhfy']
    vec = stft(vec, sfftl, sffts, ban=ban)
    ax = fig.add_subplot(335, autoscale_on=True)
    plt.imshow(vec, cmap=plt.cm.afmhot, interpolation='lanczos', aspect='auto',
               extent=[0, freq, int((len(frame['lhfx']) - sfftl) / (sfftl / sffts)), 0])

    vec = frame['lhfz']
    vec = stft(vec, sfftl, sffts, ban=ban)
    ax = fig.add_subplot(336, autoscale_on=True)
    plt.imshow(vec, cmap=plt.cm.afmhot, interpolation='lanczos', aspect='auto',
               extent=[0, freq, int((len(frame['lhfx']) - sfftl) / (sfftl / sffts)), 0])

    vec = frame['rhfx']
    vec = stft(vec, sfftl, sffts, ban=ban)
    ax = fig.add_subplot(337, autoscale_on=True)
    plt.imshow(vec, cmap=plt.cm.afmhot, interpolation='lanczos', aspect='auto',
               extent=[0, freq, int((len(frame['lhfx']) - sfftl) / (sfftl / sffts)), 0])

    vec = frame['rhfy']
    vec = stft(vec, sfftl, sffts, ban=ban)
    ax = fig.add_subplot(338, autoscale_on=True)
    plt.imshow(vec, cmap=plt.cm.afmhot, interpolation='lanczos', aspect='auto',
               extent=[0, freq, int((len(frame['lhfx']) - sfftl) / (sfftl / sffts)), 0])

    vec = frame['rhfz']
    vec = stft(vec, sfftl, sffts, ban=ban)
    ax = fig.add_subplot(339, autoscale_on=True)
    plt.imshow(vec, cmap=plt.cm.afmhot, interpolation='lanczos', aspect='auto',
               extent=[0, freq, int((len(frame['lhfx']) - sfftl) / (sfftl / sffts)), 0])

    plt.title(fl)
    plt.show()
    plt.close()


def plot_smoothed_Z_forces():
    """
    Z forzes, smoothez Zforces, difference and extrema points
    :return:
    """
    fig = plt.figure(figsize=(60, 20))
    ax = fig.add_subplot(121)
    plt.plot(range(len(frame['lhfz'])), frame['lhfz'], c='r')
    plt.plot(range(len(frame['rhfz'])), frame['rhfz'], c='b')
    plt.plot(range(len(frame['rhfz'])), frame['rhfz'] - frame['lhfz'], c='g')

    ax = fig.add_subplot(122)
    smthsig = ALS_smoothing(frame['rhfz'] - frame['lhfz'], 1, 0.1)
    plt.plot(range(len(frame['lhfz'])), ALS_smoothing(frame['lhfz'], 10, 0.1), c='r')
    plt.plot(range(len(frame['rhfz'])), ALS_smoothing(frame['rhfz'], 10, 0.1), c='b')
    plt.plot(range(len(frame['rhfz'])), smthsig, c='g')
    smax = argrelextrema(smthsig, np.greater_equal, order=5)
    smin = argrelextrema(smthsig, np.less_equal, order=5)
    vext = np.array([np.nan] * len(frame['rhfz']))
    vext[smax] = smthsig[smax]
    vext[smin] = smthsig[smin]
    plt.scatter(range(len(frame['lhfz'])), vext, marker='+', c='r')

    plt.title(fl)
    plt.show()
    plt.close()

vars = ['lhfx','lhfy','lhfz','rhfx','rhfy','rhfz','lnf','rnf','acc','magn',
        'gyro','hbl','hbr','epx','epy','epo','ls','rs']
vars2 = ['lhfx','lhfy','lhfz','rhfx','rhfy','rhfz','lnf','rnf','tilt','roll',
        'hbl','hbr','epx','epy','epo','ls','rs']


freq = 1.5
ban = 5
psfftl, psffts = 256, 64

if __name__ == '__main__':

    for ds in datasets:
        lfiles = sorted(os.listdir(odatapath+ds))
        lfiles = [f.split('.')[0] for f in lfiles if f.split('.')[1] == 'usr']

        for fl in lfiles:

            frame = pd.read_csv(odatapath+ds+fl+'.csv', sep=',')
            user = User(odatapath+ds+fl)

            print (user.get_attr('User ID'))

            #plot_forces()
            #plot_smoothed_Z_forces()

            fig = plt.figure(figsize=(60, 20))
            ax = fig.add_subplot(111, projection='3d')
            smthsigx = ALS_smoothing(frame['rhfx'] - frame['lhfx'], 1, 0.1)
            plt.plot(frame['epx'], frame['epy'], smthsigx, c='r')
            smax = argrelextrema(smthsigx, np.greater_equal, order=3)
            smin = argrelextrema(smthsigx, np.less_equal, order=3)
            vext = np.array([np.nan] * len(frame['rhfx']))
            vext[smax] = smthsigx[smax]
            vext[smin] = smthsigx[smin]
            plt.scatter(frame['epx'], frame['epy'], zs=vext, c='g', marker='o')

            smthsigx = ALS_smoothing(frame['rhfz'] - frame['lhfz'], 1, 0.1)
            plt.plot(frame['epx'], frame['epy'], smthsigx, c='b')
            smax = argrelextrema(smthsigx, np.greater_equal, order=3)
            smin = argrelextrema(smthsigx, np.less_equal, order=3)
            vext = np.array([np.nan] * len(frame['rhfx']))
            vext[smax] = smthsigx[smax]
            vext[smin] = smthsigx[smin]
            plt.scatter(frame['epx'], frame['epy'], zs=vext, c='g', marker='o')

            smthsigx = ALS_smoothing(frame['rhfy'] - frame['lhfy'], 1, 0.1)
            plt.plot(frame['epx'], frame['epy'], smthsigx, c='y')
            smax = argrelextrema(smthsigx, np.greater_equal, order=3)
            smin = argrelextrema(smthsigx, np.less_equal, order=3)
            vext = np.array([np.nan] * len(frame['rhfx']))
            vext[smax] = smthsigx[smax]
            vext[smin] = smthsigx[smin]
            plt.scatter(frame['epx'], frame['epy'], zs=vext, c='g', marker='o')
            plt.title(user.get_attr('User ID'))

            plt.show()
            plt.close()
