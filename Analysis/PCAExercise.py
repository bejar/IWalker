"""
.. module:: PlotExercise

PlotExercise
*************

:Description: PlotExercise

    

:Authors: bejar
    

:Version: 

:Created on: 30/09/2015 7:44 

"""

__author__ = 'bejar'


from pylab import *
import matplotlib.pyplot as pyplot
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from Config.Constants import datapath
from Util.Query import get_exercises_path
from sklearn.decomposition import PCA

def plot_exercise(exerdata, tied=False):
    if tied:
        maxx = np.max(exerdata[:,[0,3]])
        minx = np.min(exerdata[:,[0,3]])
        maxy = np.max(exerdata[:,[1,4]])
        miny = np.min(exerdata[:,[1,4]])
        maxz = np.max(exerdata[:,[2,5]])
        minz = np.min(exerdata[:,[2,5]])

        fig = plt.figure(figsize=(20,10))
        fig.suptitle(f)
        ax = fig.add_subplot(122, projection='3d')
        ax.set_title('Right')
        ax.set_xlabel('X')
        ax.set_xlim([minx,maxx])
        ax.set_ylabel('Y')
        ax.set_ylim([miny,maxy])
        ax.set_zlabel('Z')
        ax.set_zlim([minz,maxz])
        plt.plot(exerdata[:, 0], exerdata[:, 1], zs=exerdata[:, 2], c='r')
        ax = fig.add_subplot(121, projection='3d')
        ax.set_title('Left')
        ax.set_xlabel('X')
        ax.set_xlim([minx,maxx])
        ax.set_ylabel('Y')
        ax.set_ylim([miny,maxy])
        ax.set_zlabel('Z')
        ax.set_zlim([minz,maxz])
        plt.plot(exerdata[:, 3], exerdata[:, 4], zs=exerdata[:, 5], c='r')
        plt.show()
    else:
        fig = plt.figure(figsize=(20,10))
        fig.suptitle(f)
        ax = fig.add_subplot(122, projection='3d')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.plot(exerdata[:, 0], exerdata[:, 1], zs=exerdata[:, 2], c='r')
        ax = fig.add_subplot(121, projection='3d')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.plot(exerdata[:, 3], exerdata[:, 4], zs=exerdata[:, 5], c='r')
        plt.show()


filenames = get_exercises_path('nogales_exercise', {'d':{'$gt':0}})
#filenames = ['/idf_data/output/201407/clean/1406802774']
pca = PCA()
lpca = []
for i, f in enumerate(filenames):
    print(datapath+f)
    exerdata = loadtxt(datapath+f+'.wlk', delimiter=',')
    if len(exerdata.shape) == 2:
        pca.fit_transform(exerdata[:,[0,1,2,3,4,5]])
        lpca.append(pca.explained_variance_ratio_)
    else:
        pass


mpca = np.array(lpca)


fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.scatter(mpca[:, 0], mpca[:, 1], zs=mpca[:, 2], c='r')
plt.show()





