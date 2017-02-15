"""
.. module:: FourierExercises

FourierExercises
*************

:Description: FourierExercises

    

:Authors: bejar
    

:Version: 

:Created on: 15/10/2015 11:56 

"""

__author__ = 'bejar'



from pylab import *
import matplotlib.pyplot as pyplot
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from Util.Query_old import get_exercises_path
from numpy.fft import rfft, fftfreq
from scipy.signal import argrelextrema,argrelmax,argrelmin
from Util.Trajectory_old import straightness
from Util.STFT import stft
from numpy import loadtxt


datapath = '/home/bejar/Data/IWalker/'
def chopext(v):
    """
    Changes equal continuous values

    :param v:
    :return:
    """
    res = v.copy()
    delta=0.1
    extra=delta
    w = 0
    for i in range(1,len(v)):
        if v[w]==v[i]:
            res[i]+=extra
            extra+=delta
        else:
            w=i
            extra=delta

    return(res)

filenames = get_exercises_path('nogales_exercise', {'d':{'$gt':0}})
#filenames = get_exercises_path('idf_exercise', {'koe':'10MWT', 'd':{'$gt':0}})
#filenames = get_exercises_path('cvi_exercise', {'d':{'$gt':0}})

freq = 5.0
ban = 3
f1, f2 = 0, 3
sfftl, sffts = 128, 32

for i, f in enumerate(filenames):
    print(datapath+f)
    exerdata = loadtxt(datapath+f+'.wlk', delimiter=',')
    print(straightness(exerdata[:,[12,13]])[0])
    if exerdata.shape[0]> sfftl and 0.97 <straightness(exerdata[:,[12,13]])[0]<1:
        exerdata.shape
        # fuerza 1
        var1 = exerdata[:, f1]
        trans = rfft(var1)
        fig = plt.figure(figsize=(20,10))
        ax = fig.add_subplot(331)
        lim= fftfreq(var1.shape[0],d=0.1)
        plt.plot(lim[0:trans.shape[0]-2], np.abs(trans[0:-2]))
        ax = fig.add_subplot(332)
        plt.plot(np.array(range(var1.shape[0]))/10.0, var1)
        res = chopext(var1)
        smax = argrelextrema(res, np.greater_equal, order=5)
        smin = argrelextrema(res, np.less_equal, order=5)
        vext = np.array([np.nan]*var1.shape[0])
        vext[smax] = var1[smax]
        vext[smin] = var1[smin]
        plt.scatter(np.array(range(var1.shape[0]))/10.0, vext,marker='+',c='r')
        vec = stft(var1, sfftl, sffts, ban=ban)
        ax = fig.add_subplot(333)
        plt.imshow(vec, cmap=plt.cm.afmhot, interpolation='lanczos', aspect='auto', extent=[0,freq,int((var1.shape[0]-sfftl)/(sfftl/sffts)), 0])

        # fuerza 2
        var2 = exerdata[:, f2]
        trans = rfft(var2)
        ax = fig.add_subplot(334)
        lim= fftfreq(var2.shape[0], d=0.1)
        plt.plot(lim[0:trans.shape[0]-2], np.abs(trans[0:-2]))
        ax = fig.add_subplot(335)
        plt.plot(np.array(range(var2.shape[0]))/10.0, var2)
        res = chopext(var2)
        smax = argrelextrema(res, np.greater_equal, order=5)
        smin = argrelextrema(res, np.less_equal, order=5)
        vext = np.array([np.nan]*var2.shape[0])
        vext[smax] = var2[smax]
        vext[smin] = var2[smin]
        plt.scatter(np.array(range(var2.shape[0]))/10.0, vext,marker='+',c='r')
        vec = stft(var2, sfftl, sffts, ban=ban)
        ax = fig.add_subplot(336, autoscale_on=True)
        plt.imshow(vec, cmap=plt.cm.afmhot, interpolation='lanczos', aspect='auto', extent=[0,freq,int((var1.shape[0]-sfftl)/(sfftl/sffts)), 0])

        # trayectoria
        ax = fig.add_subplot(338)
        plt.plot(exerdata[:,12], exerdata[:,13])
        plt.scatter(exerdata[0,12], exerdata[0,13], marker='+', c='g')
        plt.scatter(exerdata[-1,12], exerdata[-1,13], marker='+', c='r')

        ax.set_aspect('equal', 'datalim')

        plt.show()
    else:
        if exerdata.shape[0]< sfftl:
            print('Too Short', exerdata.shape)
