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
import seaborn as sb
from pylab import *
import numpy as np
from Util.STFT import stft
import matplotlib.gridspec as gridspec
from Util.Smoothing import ALS_smoothing, numpy_smoothing
from scipy.signal import argrelextrema
from Util import User, Exercise, Exercises, Pacientes

def total_norm(x, y, z):
    return np.sqrt(x*x+y*y+z*z)


def cosinus_angle(x1,y1,z1,x2,y2,z2):
    return((x1*x2+y1*y2+z1*z2) /(total_norm(x1,y1,z1)*total_norm(x2,y2,z2)))



def plot_forces(frame):
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
            sfftl /= 2

        sffto = psffto / 4
    else:
        sfftl = psfftl
        sffto = psffto

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
    vec = stft(vec, sfftl, sffto, ban=ban)
    ax = fig.add_subplot(334, autoscale_on=True)
    plt.imshow(vec, cmap=plt.cm.afmhot, interpolation='lanczos', aspect='auto',
                extent=[0, freq, int((len(frame['lhfx']) - sfftl) / (sfftl / sffto)), 0])

    vec = frame['lhfy']
    vec = stft(vec, sfftl, sffto, ban=ban)
    ax = fig.add_subplot(335, autoscale_on=True)
    plt.imshow(vec, cmap=plt.cm.afmhot, interpolation='lanczos', aspect='auto',
               extent=[0, freq, int((len(frame['lhfx']) - sfftl) / (sfftl / sffto)), 0])

    vec = frame['lhfz']
    vec = stft(vec, sfftl, sffto, ban=ban)
    ax = fig.add_subplot(336, autoscale_on=True)
    plt.imshow(vec, cmap=plt.cm.afmhot, interpolation='lanczos', aspect='auto',
               extent=[0, freq, int((len(frame['lhfx']) - sfftl) / (sfftl / sffto)), 0])

    vec = frame['rhfx']
    vec = stft(vec, sfftl, sffto, ban=ban)
    ax = fig.add_subplot(337, autoscale_on=True)
    plt.imshow(vec, cmap=plt.cm.afmhot, interpolation='lanczos', aspect='auto',
               extent=[0, freq, int((len(frame['lhfx']) - sfftl) / (sfftl / sffto)), 0])

    vec = frame['rhfy']
    vec = stft(vec, sfftl, sffto, ban=ban)
    ax = fig.add_subplot(338, autoscale_on=True)
    plt.imshow(vec, cmap=plt.cm.afmhot, interpolation='lanczos', aspect='auto',
               extent=[0, freq, int((len(frame['lhfx']) - sfftl) / (sfftl / sffto)), 0])

    vec = frame['rhfz']
    vec = stft(vec, sfftl, sffto, ban=ban)
    ax = fig.add_subplot(339, autoscale_on=True)
    plt.imshow(vec, cmap=plt.cm.afmhot, interpolation='lanczos', aspect='auto',
               extent=[0, freq, int((len(frame['lhfx']) - sfftl) / (sfftl / sffto)), 0])

    plt.title(ex.uid + '/' + str(ex.id))
    plt.show()
    plt.close()


def plot_smoothed_Z_forces(frame):
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
    # smthsig = numpy_smoothing(ALS_smoothing(frame['rhfz'] - frame['lhfz'], 1, 0.1)
    # plt.plot(range(len(frame['lhfz'])), ALS_smoothing(frame['lhfz'], 10, 0.1), c='r')
    # plt.plot(range(len(frame['rhfz'])), ALS_smoothing(frame['rhfz'], 10, 0.1), c='b')

    smthsig = numpy_smoothing(frame['rhfz'] - frame['lhfz'], window_len=11, window='blackman')
    plt.plot(range(len(frame['lhfz'])), numpy_smoothing(frame['lhfz'], window_len=5, window='blackman'), c='r')
    plt.plot(range(len(frame['rhfz'])), numpy_smoothing(frame['rhfz'], window_len=5, window='blackman'), c='b')

    plt.plot(range(len(frame['rhfz'])), smthsig, c='g')
    smax = argrelextrema(smthsig, np.greater_equal, order=5)
    smin = argrelextrema(smthsig, np.less_equal, order=5)
    vext = np.array([np.nan] * len(frame['rhfz']))
    vext[smax] = smthsig[smax]
    vext[smin] = smthsig[smin]
    plt.scatter(range(len(frame['lhfz'])), vext, marker='+', c='r')
    plt.title(ex.uid + '/' + str(ex.id))

    plt.show()
    plt.close()

def plot_smoothed_forces_with_extrema(frame):
    """
    L-R XYZ forces smoothed with extrema points

    :return:
    """
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
    plt.title(ex.uid + '/' + str(ex.id))

    plt.show()
    plt.close()

def plot_correlation(frame):
    """
    Trajectory and correlation of the forces

    :return:
    """


    fig = plt.figure(figsize=(20, 40))
    ax = fig.add_subplot(121)
    plt.plot(frame['epx'], frame['epy'], c='r')
    ax = fig.add_subplot(122)

    sb.heatmap(frame.corr().abs(), vmax=1, square=True)
    plt.title(ex.uid + '/' + str(ex.id))
    plt.show()
    plt.close()


def do_it_from_files():
    '''
    Loads and presents the data from the csv files
    :return:
    '''
    for ds in datasets:
        lfiles = sorted(os.listdir(odatapath+ds))
        lfiles = [f.split('.')[0] for f in lfiles if f.split('.')[1] == 'usr']

        for fl in lfiles:
            ex = Exercise()
            ex.from_file(odatapath+ds+fl)

            print (ex.uid)

            #plot_forces(ex.frame)

            #plot_smoothed_Z_forces(ex.frame)

            #plot_smoothed_forces_with_extrema(ex.frame)

            plot_correlation(ex.frame)

vars = ['lhfx','lhfy','lhfz','rhfx','rhfy','rhfz','lnf','rnf','acc','magn',
        'gyro','hbl','hbr','epx','epy','epo','ls','rs']
vars2 = ['lhfx','lhfy','lhfz','rhfx','rhfy','rhfz','lnf','rnf','tilt','roll',
        'hbl','hbr','epx','epy','epo','ls','rs']


freq = 10/2  # Half the sampling frequence

psfftl, psffto = 64, 48


print('Freq Resolution=',((freq*1.0)/psfftl))
# Ban frequencies below 0.25 Hz
ban = int(0.25 / ((freq*1.0)/psfftl))-1

if __name__ == '__main__':

    p = Pacientes()
    e = Exercises()
    p.from_db(pilot='NOGA')
    e.from_db(pilot='NOGA')
    # e.delete_patients(['FSL30'])

    for ex in e.iterator():

        print (ex.uid+ '-' + str(ex.id))

        #plot_forces(ex.frame)

        #plot_smoothed_Z_forces(ex.frame)

        #plot_smoothed_forces_with_extrema(ex.frame)

        #plot_correlation(ex.frame)


        fig = plt.figure(figsize=(60, 20))
        ax = fig.add_subplot(111)
        plt.plot(range(len(ex.frame['lhfz'])), ex.compute_speed(0.1), c='r')
        plt.plot(range(len(ex.frame['rhfz'])), ex.frame['rs'], c='b')
        plt.plot(range(len(ex.frame['rhfz'])), ex.frame['ls'], c='g')
        plt.title(ex.uid + '/' + str(ex.id))
        plt.show()
        plt.close()
