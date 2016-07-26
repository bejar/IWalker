"""
.. module:: Exercises

Exercises
*************

:Description: Exercises

    

:Authors: bejar
    

:Version: 

:Created on: 26/07/2016 11:48 

"""


from pymongo import MongoClient
from Config.Private import mongoserverlocal
from Util import Exercise

__author__ = 'bejar'

class Exercises:

    def __init__(self):
        pass

    def from_db(self, pilot=None):
        """
        Gets a set of exercises from the DB

        :param pilot:
        :param user:
        :return:
        """

        client = MongoClient(mongoserverlocal)
        db = client.IWalker
        col = db['Exercises']
        if pilot is None:
            c = col.find()
        else:
            c = col.find({'User ID': {'$regex': pilot + '.*'}})


        self.edict = {}

        for d in c:
            e = Exercise()
            e.from_data(d)
            self.edict[d['Unix Time']] = e


    def iterator(self):
        """
        Patients iterator

        :return:
        """
        for p in self.edict:
            yield self.edict[p]


if __name__ == '__main__':
    p = Exercises()

    p.from_db(pilot='NOGALES46')

    for v in p.iterator():
        print(v.uid)
