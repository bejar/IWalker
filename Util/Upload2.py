"""
.. module:: Upload2

Upload2
*************

:Description: Upload2

    

:Authors: bejar
    

:Version: 

:Created on: 26/07/2016 9:59 

"""

__author__ = 'bejar'


import os
from pymongo import MongoClient
from Config.Constants import odatapath, datasets, datasets2
from Config.Connection import mongoserverlocal
from Util import User, Pacientes
import pandas as pd


def upload_patients():
    """
    Uploads to Mongo the csv file with the patients

    :return:
    """
    col = db['Users']
    p = Pacientes(odatapath+'pacientes')
    for d in p.ddict:
        col.insert(p.ddict[d])

if __name__ == '__main__':


    client = MongoClient(mongoserverlocal)
    db = client.IWalker


    col = db['Exercises']


    for ds in datasets2:
        lfiles = sorted(os.listdir(odatapath+ds))
        lfiles = [f.split('.')[0] for f in lfiles if f.split('.')[1] == 'usr']

        for fl in lfiles:

            frame = pd.read_csv(odatapath+ds+fl+'.csv', sep=',')
            user = User(odatapath+ds+fl)
            print (user.get_attr('User ID'))
            data = {}
            data['User ID'] = user.get_attr('User ID')
            data['Unix Time'] = user.get_attr('Unix Time')
            data['i-Walker lambda_left'] = user.get_attr('i-Walker lambda_left')
            data['i-Walker lambda_right'] = user.get_attr('i-Walker lambda_right')
            if user.exist_attr('Gender'):
                data['Gender'] = user.get_attr('Gender')
            if user.exist_attr('Laterality'):
                data['Laterality'] = user.get_attr('Laterality')
            if user.exist_attr('Exercise'):
                data['Exercise'] = user.get_attr('Exercise')

            f = open(odatapath + ds + '/' + fl + '.csv', 'r')
            datastr = ''
            for line in f:
                datastr += line
            data['csv'] = datastr
            col.insert(data)

