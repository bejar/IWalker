"""
.. module:: Explore

Explore
*************

:Description: Explore

    

:Authors: bejar
    

:Version: 

:Created on: 21/09/2015 15:14 

"""

__author__ = 'bejar'


from pymongo import MongoClient
from Config.Connection import mongopass, mongouser
client = MongoClient('mongodb-rdlab.lsi.upc.edu')

db = client.iwalkersws

db.authenticate(mongouser, password=mongopass)

col = db['idf_exercise']

lres = col.find({'koe':{'$regex':'10MWT'}},{'koe':1, 'path':1})

tmres = []

for v in lres:
    tmres.append(v['path'])
    print(v['path'])






