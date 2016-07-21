"""
.. module:: GetExercises

GetExercises
*************

:Description: GetExercises

    

:Authors: bejar
    

:Version: 

:Created on: 30/09/2015 7:31 

"""

__author__ = 'bejar'

import os

import paramiko
from pymongo import MongoClient

from Config.Private import username, password, machine, mongopass, mongouser, mongoserver

localdir = '/home/bejar/Data/IWalker/'
exts = ['.wlk', '_eq.wlk']
#exts = ['.wlk']

client = MongoClient(mongoserver)
db = client.iwalkersws
db.authenticate(mongouser, password=mongopass)

# 'idf_exercise' 'nogales_exercise' 'cvi_exercise'
col = db['idf_exercise']
# {'koe': {'$regex': '10MWT'}}, {'koe': 1, 'path': 1}
lres = col.find({'koe': {'$regex': '10MWT'}}, {'koe': 1, 'path': 1})

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(machine, username=username, password=password)
sftp = ssh.open_sftp()

for v in lres:
    pfile = v['path']
    elems = pfile.split('/')
    print(pfile)
    filename = elems[-1].split('.')[0]

    remotedir = '/' + elems[1] + '/' + elems[2] + '/'
    addpath = ''
    for e in elems[3:-1]:
        addpath += e + '/'
    if not os.path.exists(localdir + addpath):
        os.makedirs(localdir + addpath)
    for e in exts:
        print(remotedir + addpath + filename + e)
        sftp.get(remotedir + addpath + filename + e, localdir + addpath + filename + e)
