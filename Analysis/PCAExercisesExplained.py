"""
.. module:: PCAExercises

PlotExercise
*************

:Description: PCAExercises

  Plot of the explained variance using 3 PCA components of the exercises of the query

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
from Util.Query_old import get_exercises_info, get_site_exercises_info
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


def compute_PCA_exercises(users, limit=None):
    """
    Computes the matrix of explained variance by the tree first components of PCA of each exercise
    :return:
    """
    pca = PCA()
    lpca = []
    labels = []
    for u in users:
        lex = sorted(users[u], key=lambda us: us[0])
        lpaths = [path for _, path in lex]
    #    print(len(lpaths))
        for i, f in enumerate(lpaths):
            # only the three first exercises of each individual
            if i <3:
                exerdata = loadtxt(datapath+f+'.wlk', delimiter=',')
                distance = loadtxt(datapath+f+'_eq.wlk', delimiter=',')
                if len(exerdata.shape) == 2:
                    distance = distance[:,-2]
                    distance /= np.max(distance)
                    if not limit:
                        rows = range(exerdata.shape[0])
                    else:
                        rows = [j for j in range(exerdata.shape[0]) if limit[0] <= distance[j] <= limit[1]]

                    exerdata = exerdata[rows,:]
                    if exerdata.shape[0] > 6:
                        pca.fit_transform(exerdata[:,[0,1,2,3,4,5]])
                        lpca.append(pca.explained_variance_ratio_)
                        labels.append(i)
                else:
                    pass


    return np.array(lpca), np.array(labels)

if __name__ == '__main__':

    #users = get_exercises_info('idf', {'koe': '10MWT', 'd':{'$gt':0}})
    #users = get_exercises_info('cvi_exercise', { 'd':{'$gt':0}})
    users = get_site_exercises_info('idf', 'FSM', {'koe': '10MWT', 'd':{'$gt':0}})

    mpca, labels = compute_PCA_exercises(users, limit=[0.2, 0.8])

    fig = plt.figure(figsize=(30,10))
    ax = fig.add_subplot(131, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.scatter(mpca[labels==0, 0], mpca[labels==0, 1], zs=mpca[labels==0, 2], c=labels[labels==0], depthshade=False, s=20)
    ax = fig.add_subplot(132, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.scatter(mpca[labels==1, 0], mpca[labels==1, 1], zs=mpca[labels==1, 2], c=labels[labels==1], depthshade=False, s=20)
    ax = fig.add_subplot(133, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.scatter(mpca[labels==2, 0], mpca[labels==2, 1], zs=mpca[labels==2, 2], c=labels[labels==2], depthshade=False, s=20)
    plt.show()





