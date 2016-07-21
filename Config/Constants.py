"""
.. module:: Config

Config
*************

:Description: Config

    

:Authors: bejar
    

:Version: 

:Created on: 30/09/2015 7:54 

"""

__author__ = 'bejar'

# Path to the datafiles
datapath = '/home/bejar/Data/IWalker/'

# extensions of the data files
exts = ['.wlk', '_eq.wlk']


odatapath = '/home/bejar/storage/Data/IWalker/'

datasets = ['fsl_output/PZ/', 'fsl_output/HC/']
datasetso = ['fsl_orig/PZ/', 'fsl_orig/HC/']

datasets2 = ['mad_output/201502/', 'mad_output/201503/']
datasets2o = ['mad_output_orig/201502/', 'mad_output_orig/201503/']

datasets3 = ['straights_output/']
datasets3o = ['straights_output_orig/']


from Config.Constants import odatapath,  datasets2o, datasets2, datasets3o, datasets3
import os

__author__ = 'bejar'


for ds, pds in zip(datasets3o,datasets3):
    print(odatapath+ds)
    lfiles = sorted(os.listdir(odatapath+ds))
