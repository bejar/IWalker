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
from sklearn.manifold import MDS, SpectralEmbedding
from sklearn.cluster import KMeans
from Util.User import User
from Util.Pacientes import Pacientes

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


# 4 4 3 32

step = 4
word_length = 4
voc_size = 3
window_length = 16


#attr = ['lhfx', 'lhfy', 'lhfz', 'rhfx', 'rhfy', 'rhfz']
attr = ['lhfx', 'lhfy', 'lhfz', 'rhfx', 'rhfy', 'rhfz']

labels = []
lvec = []
l = 0

p = Pacientes(odatapath+'pacientes')
exid = []

for ds in datasets:
    lfiles = os.listdir(odatapath+ds)
    lfiles = [f.split('.')[0] for f in lfiles if f.split('.')[1] == 'usr']
    sax = SAX(window_length=window_length, step=step, word_length=word_length, voc_size=voc_size)


    for fl in lfiles:
        frame = pd.read_csv(odatapath+ds+fl+'.csv', sep=',')
        user = User(odatapath+ds+fl)
        caida = p.get_patient_attribute(user.get_attr('User ID'), 'Caidas')

        nwin = (len(frame['lhfx']-window_length)//step) + 1
        if nwin > 10 and caida is not None:
            exid.append(user.get_attr('User ID')+'/'+str(user.get_attr('Unix Time')))
            # labels.append(int(fl.split('_')[0])%4)
            if  caida != 0:
                labels.append(1)
            else:
                labels.append(0)
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
    l += 1
data = np.array(lvec)
print data.shape, len(labels)

pca = PCA(n_components=0.9)
#pca = MDS(n_components=3)
#pca = SpectralEmbedding(n_components=3, n_neighbors=5)

data = pca.fit_transform(data)
print(pca.n_components_)
fig = plt.figure(figsize=(20, 20))

ax = fig.add_subplot(111, projection='3d')

plt.scatter(data[:, 0], data[:, 1], zs=data[:, 2], c=labels, marker='o')

plt.show()
plt.close()

km = KMeans(n_clusters=3)

km.fit_predict(data)

for ex, lab in zip(exid, km.labels_):
    print(ex, lab)

