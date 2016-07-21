"""
.. module:: SAXExperiment

SAXExperiment
*************

:Description: SAXExperiment

    

:Authors: bejar
    

:Version: 

:Created on: 19/07/2016 13:48 

"""

from Config.Constants import odatapath, datasets, datasets2, datasets3
import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
import numpy as np
from Util.STFT import stft
import matplotlib.gridspec as gridspec
from kemlglearn.time_series.discretization import SAX
from sklearn.decomposition import PCA
from sklearn.manifold import MDS

__author__ = 'bejar'

def index(vec, base):
    """
    Tranforms a vector representing a number in base b to an index in decimal
    :param vec:
    :return:
    """
    index = 0
    for i in range(len(vec)):
        index += (vec[i]*(base**i))
    return int(index)

step = 4
word_length = 4
voc_size = 3
window_length = 32


#attr = ['lhfx', 'lhfy', 'lhfz', 'rhfx', 'rhfy', 'rhfz']
attr = ['lhfx', 'lhfy', 'lhfz', 'rhfx', 'rhfy', 'rhfz']

labels = []
lvec = []

for ds in datasets:
    lfiles = os.listdir(odatapath+ds)
    sax = SAX(window_length=window_length, step=step, word_length=word_length, voc_size=voc_size)


    for fl in lfiles:

        frame = pd.read_csv(odatapath+ds+fl, sep=',')
        nwin = (len(frame['lhfx']-window_length)//step) + 1
        if nwin > 10:
            print(fl, fl.split('_')[0])
            labels.append(int(fl.split('_')[0])%4)
            wrd_attr = np.array([])
            for v in attr:
                sax_trans = sax.transform(frame[v])
                wrd_dist = np.zeros(voc_size**word_length)
                for vec in sax_trans:
                    vec += voc_size/2
                    wrd_dist[index(vec, voc_size)] += 1

                wrd_dist /= len(sax_trans)
                wrd_attr = np.append(wrd_attr, wrd_dist)

            lvec.append(wrd_attr)
data = np.array(lvec)
print data.shape, len(labels)

#pca = PCA(n_components=0.9)
pca = MDS(n_components=3)

data = pca.fit_transform(data)
#print(pca.n_components_)
fig = plt.figure(figsize=(20, 20))

ax = fig.add_subplot(111, projection='3d')

plt.scatter(data[:, 0], data[:, 1], zs=data[:, 2], c=labels, marker='o')

plt.show()
plt.close()
