"""
.. module:: Exercise

Exercise
*************

:Description: Exercise

    

:Authors: bejar
    

:Version: 

:Created on: 26/07/2016 10:06 

"""

import pandas as pd
from pymongo import MongoClient
from Config.Private import mongoserverlocal
from io import StringIO
from Util import User

__author__ = 'bejar'



class Exercise:
    """
    Class representing the data from an exercise
    """

    def __init__(self):
        pass


    def from_data(self, ex):
        self.uid = ex['User ID']
        self.id = ex['Unix Time']
        self.frame = pd.read_csv(StringIO(ex['csv']), sep=',')

    def from_file(self, dfile):
        self.user = User(dfile)
        self.id = self.user.get_attr('Unix Time')
        self.uid = self.user.get_attr('User ID')

        self.frame = pd.read_csv(dfile+'.csv', sep=',')

    def from_db(self, id):
        client = MongoClient(mongoserverlocal)
        db = client.IWalker
        col = db['Exercises']
        c = col.find_one({'Unix Time':id})

        self.id = id
        self.frame = pd.read_csv(StringIO(c['csv']), sep=',')
        self.uid = c['User ID']


