"""
.. module:: SAXExperiment

SAXExperiment
*************

:Description: SAXExperiment

    

:Authors: bejar
    

:Version: 

:Created on: 26/07/2016 13:03 

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
from kemlglearn.time_series.discretization import SAX
from sklearn.decomposition import PCA, NMF
from sklearn.manifold import MDS, SpectralEmbedding
from sklearn.cluster import KMeans
from sklearn.mixture import GMM, DPGMM
from Util import Pacientes, Exercises

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


def compute_label(caida, lamb):
    """

    :param caida:
    :param lamb:
    :return:
    """
    if lamb == 0:
        if caida == 0:
            return 'm'
        else:
            return 'r'
    elif lamb <30:
        if caida == 0:
            return 'y'
        else:
            return 'g'
    else:
        if caida == 0:
            return 'c'
        else:
            return 'b'


# 4 4 3 32

step = 4
word_length = 4
voc_size = 3
window_length = 32


#attr = ['lhfx', 'lhfy', 'lhfz', 'rhfx', 'rhfy', 'rhfz']
attr = ['lhfx', 'lhfy', 'lhfz', 'rhfx', 'rhfy', 'rhfz']

labels = []
lvec = []
l = 0

exid = []

laplace = 0.0001

p = Pacientes()
e = Exercises()

# p.from_db(pilot='FSL')
# e.from_db(pilot='FSL')
# e.delete_patients(['FSL30'])
# e.delete_exercises([1416935335])

p.from_db(pilot='NOGA')
e.from_db(pilot='NOGA')


sax = SAX(window_length=window_length, step=step, word_length=word_length, voc_size=voc_size)

for ex in e.iterator():
    caida = p.get_patient_attribute(ex.uid, 'Caidas')
    lamb = ex.lamb

    nwin = (len(ex.frame['lhfx']-window_length)//step) + 1
    # print(nwin)
    if nwin > 10 and (caida is not None):
        exid.append(ex.uid+'/'+str(ex.id))
        # labels.append(int(fl.split('_')[0])%4)
        labels.append(compute_label(caida, lamb))

        wrd_attr = np.array([])
        for v in attr:
            sax_trans = sax.transform(ex.frame[v])
            wrd_dist = np.zeros(voc_size**word_length) + laplace
            for vec in sax_trans:
                vec += voc_size/2
                wrd_dist[index(vec, voc_size)] += 1

            wrd_dist /= np.sum(wrd_dist)
            wrd_attr = np.append(wrd_attr, wrd_dist)

        lvec.append(wrd_attr)

data = np.array(lvec)
print data.shape, len(labels)

#pca = PCA(n_components=0.9)
#pca = MDS(n_components=3)
#pca = SpectralEmbedding(n_components=3, n_neighbors=3)
pca = NMF(n_components=20)

datat = pca.fit_transform(data)

# print(pca.n_components_)
# print(pca.explained_variance_ratio_[0:3])
print(pca.reconstruction_err_)

fig = plt.figure(figsize=(20, 20))

ax = fig.add_subplot(111, projection='3d')

plt.scatter(datat[:, 0], datat[:, 1], zs=datat[:, 2], c=labels, marker='o')

plt.show()
plt.close()

#km = KMeans(n_clusters=5)

km = DPGMM(n_components=7, covariance_type='tied')

clabels = km.fit_predict(datat)

# for ex, lab in zip(exid, clabels):
#     print(ex, lab)

fig = plt.figure(figsize=(20, 20))

ax = fig.add_subplot(111, projection='3d')

plt.scatter(datat[:, 0], datat[:, 1], zs=datat[:, 2], c=clabels, marker='o')

plt.show()
plt.close()
