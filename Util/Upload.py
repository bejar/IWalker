"""
.. module:: Upload

Upload
*************

:Description: Upload

    

:Authors: bejar
    

:Version: 

:Created on: 05/07/2016 10:59 

"""


import os
from pymongo import MongoClient
from Config.Constants import odatapath, datasets
from Config.Private import mongoserverlocal
from io import StringIO

import pandas as pd
__author__ = 'bejar'

header = 'lhfx,lhfy,lhfz,rhfx,rhfy,rhfz,lnf,rnf,acc,magn,gyro,hbl,hbr,epx,epy,epo,ls,rs\n'


def is_int(v):
    try:
        a = int(v)
        return True
    except ValueError:
        return False

def is_float(v):
    try:
        a = float(v)
        return True
    except ValueError:
        return False

client = MongoClient(mongoserverlocal)
db = client.IWalker
col = db['Data']


for ds in datasets:
    lfiles = sorted(os.listdir(odatapath+ds))
    lfiles = [f.split('.')[0] for f in lfiles if f.split('.')[1] == 'usr']
    for fl in lfiles:
        f = open(odatapath + ds + '/' + fl + '.usr', 'r')
        data = {}
        for line in f:
            vals = line.split(':')
            if is_int(vals[1].strip()):
                data[vals[0].strip()] = int(vals[1].strip())
            elif is_float(vals[1].strip()):
                data[vals[0].strip()] = float(vals[1].strip())
            else:
                data[vals[0].strip()] = vals[1].strip()
        f.close()
        f = open(odatapath + ds + '/' + fl + '.csv', 'r')
        datastr = header
        for line in f:
            datastr += line
        data['csv'] = datastr
        print(data)
        col.insert(data)




