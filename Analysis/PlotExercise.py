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
import seaborn as sns
import matplotlib.pyplot as plt
from Util.Trajectory_old import geodesic, parametric_select, straightness, convex_hull


def plot_exercise(exerdata, distance, tied=False, limit=None):
    dmax = np.max(distance)
    if tied:
        distance /= np.max(distance)
        if not limit:
            rows = range(exerdata.shape[0])
        else:
            rows = [i for i in range(exerdata.shape[0]) if limit[0]<=distance[i]<=limit[1]]

        print(exerdata.shape)
        exerdata = exerdata[rows,:]
        print(exerdata.shape)

        distance = distance[rows]

        maxx = np.max(exerdata[:, [0,3]])
        minx = np.min(exerdata[:, [0,3]])
        maxy = np.max(exerdata[:, [1,4]])
        miny = np.min(exerdata[:, [1,4]])
        maxz = np.max(exerdata[:, [2,5]])
        minz = np.min(exerdata[:, [2,5]])

        fig = plt.figure(figsize=(20,10))
        fig.suptitle(f + ' (' + str(dmax) + ')')

        ax = fig.add_subplot(122, projection='3d')
        ax.set_title('Right')
        ax.set_xlabel('X')
        ax.set_xlim([minx,maxx])
        ax.set_ylabel('Y')
        ax.set_ylim([miny,maxy])
        ax.set_zlabel('Z')
        ax.set_zlim([minz,maxz])
        plt.plot(exerdata[:, 0], exerdata[:, 1], zs=exerdata[:, 2], color='k')
        plt.scatter(exerdata[:, 0], exerdata[:, 1], zs=exerdata[:, 2], c=distance, s=50)
        ax = fig.add_subplot(121, projection='3d')
        ax.set_title('Left')
        ax.set_xlabel('X')
        ax.set_xlim([minx,maxx])
        ax.set_ylabel('Y')
        ax.set_ylim([miny,maxy])
        ax.set_zlabel('Z')
        ax.set_zlim([minz,maxz])
        plt.plot(exerdata[:, 3], exerdata[:, 4], zs=exerdata[:, 5], color='k')
        plt.scatter(exerdata[:, 3], exerdata[:, 4], zs=exerdata[:, 5], c=distance,s=50)
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

def plot_exercise_movement(vec):
    mx = np.sum(vec[:,0])/(vec.shape[0]*1.0)
    my = np.sum(vec[:,1])/(vec.shape[0]*1.0)
    otocdm = np.sqrt(((vec[0,0] - mx)**2) + ((vec[0,1] - my)**2))
    ftocdm = np.sqrt(((vec[-1,0] - mx)**2) + ((vec[-1,1] - my)**2))
    euc = otocdm + ftocdm
    euc2 = np.sqrt(((vec[-1,0] - vec[0,0])**2) + ((vec[-1,1] - vec[0,1])**2))
    geo = geodesic(vec)
    print('BE-R= %f CDM-R= %f ' %(euc2/geo, euc/geo))

    fig = plt.figure(figsize=(20,10))
    fig.suptitle(f)
    ax = fig.add_subplot(111)
    plt.plot(vec[:, 0], vec[:, 1])
    plt.scatter(vec[:, 0], vec[:, 1])
    plt.scatter(mx, my, color='r', marker='+')
    plt.plot([vec[0,0], mx], [vec[0,1],my], color='r')
    plt.plot([vec[-1,0], mx], [vec[-1,1],my], color='r')
    ax.set_aspect('equal', 'datalim')

    ch = convex_hull(vec)
    plt.plot(ch[:,0], ch[:,1], color='g')
    plt.show()



#filenames = get_exercises_path('idf_exercise', {'koe':'10MWT', 'd':{'$gt':0}})
filenames = get_exercises_path('nogales_exercise', {'d':{'$gt':0}})
#filenames = get_exercises_path('cvi_exercise', {'d':{'$gt':0}})
# filenames = ['/idf_data/output/201407/clean/1406802774']

lstraigh = []
for f in filenames:
    exerdata2 = loadtxt(datapath+f+'_eq.wlk', delimiter=',')
    exerdata = loadtxt(datapath+f+'.wlk', delimiter=',')

    distance= exerdata2[:, -2]
    trajectory = parametric_select(exerdata[:,[12,13]], distance, 0, 1)
    #print(exerdata.shape[0], trajectory.shape[0])
    # if np.max(trajectory)>200000 or np.min(trajectory)<-200000:
    #     print(f)
    #     plot_exercise_movement(trajectory)
    r1, r2 = straightness(trajectory)
#    print('%s R1= %f, R2= %f' % (datapath+f, r1, r2))
    lstraigh.append(r1)



    if 0.95 < r1 < 0.98: # len(exerdata.shape[1]) > 2:
#        plot_exercise(exerdata[:,[0,1,2,3,4,5]], exerdata2[:,-2], tied=True, limit=[0.2,0.8])

        plot_exercise_movement(trajectory)

    else:
         pass



fig = plt.figure(figsize=(20,30))
sns.distplot(lstraigh, hist=False, rug=True, color="g", kde_kws={"shade": True})
plt.show()