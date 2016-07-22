"""
.. module:: Mtch

Mtch
*************

:Description: Mtch

    

:Authors: bejar
    

:Version: 

:Created on: 22/07/2016 12:09 

"""

__author__ = 'bejar'


from Config.Constants import odatapath, datasets, datasets2, datasets3, datasets3o
from pylab import *
from Util.User import User
import os



ds2 = {}

for ds in datasets2:
    lfiles = sorted(os.listdir(odatapath+ds))
    lfiles = [f.split('.')[0] for f in lfiles if f.split('.')[1] == 'usr']
    for fl in lfiles:
        user = User(odatapath+ds+fl)
        if user.get_attr('User ID') not in ds2:
            ds2[user.get_attr('User ID')] = [user.get_attr('Unix Time')]
        else:
            ds2[user.get_attr('User ID')].append(user.get_attr('Unix Time'))

ds3 = {}

for ds in datasets3o:
    lfiles = sorted(os.listdir(odatapath+ds))
    lfiles = [f.split('.')[0] for f in lfiles if f.split('.')[1] == 'usr']
    for fl in lfiles:
        user = User(odatapath+ds+fl)
        if user.get_attr('User ID') not in ds2:
            ds3[user.get_attr('User ID')] = [user.get_attr('Unix Time')]
        else:
            ds3[user.get_attr('User ID')].append(user.get_attr('Unix Time'))

lc = []
for v in ds2:
    for v2 in ds3:
        found = False
        for e in ds2[v]:
            if e in ds3[v2]:
                found = True
                break
        if found:
            lc.append((v, v2))
print(sorted(lc))