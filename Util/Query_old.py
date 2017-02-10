"""
.. module:: Query

Query
*************

:Description: Query

    

:Authors: bejar
    

:Version: 

:Created on: 30/09/2015 8:52 

"""

__author__ = 'bejar'

from pymongo import MongoClient
from bson.objectid import ObjectId

from Config.Connection import mongopass, mongouser, mongoserver

def convert_path(pfile):
    """
    Translates IDF path to relative path

    :param path:
    :return:
    """
    elems = pfile.split('/')
    filename = elems[-1].split('.')[0]
    addpath = ''
    for e in elems[3:-1]:
        addpath += e + '/'

    return(addpath+filename)

def get_exercises_path(site, query):
    """
    Returns a list with the relative paths of the exercises of a specific query
    relative to the datapath

    :param site:
    :param query:
    :return:
    """
    client = MongoClient(mongoserver)
    db = client.iwalkersws
    db.authenticate(mongouser, password=mongopass)
    col = db[site]
    lres = col.find(query, {'path': 1})

    lpaths = []
    for v in lres:
        pfile = v['path']
        elems = pfile.split('/')
        filename = elems[-1].split('.')[0]
        addpath = ''
        for e in elems[3:-1]:
            addpath += e + '/'
        lpaths.append(addpath+filename)
    return lpaths


def get_exercises_info(site, query):
    """
    Returns a diccionary indexed by user id each entry with a list of pairs
    (timestamp, relative path to the exercise)

    :param site:
    :param query:
    :return:
    """
    client = MongoClient(mongoserver)
    db = client.iwalkersws
    db.authenticate(mongouser, password=mongopass)
    col = db['%s_exercise'%site]
    lres = col.find(query, {'path': 1, 'user_id': 1, 'ts': 1})

    dres = {}
    for v in lres:
        user = v['user_id']
        if user in dres:
            dres[user].append((v['ts'],convert_path(v['path'])))
        else:
            dres[user] = [(v['ts'],convert_path(v['path']))]
    return dres


def get_pilot_id(site, pilot):
    """
    Gets the ID of a pilot :-)
    :param site:
    :return:
    """
    client = MongoClient(mongoserver)
    db = client.iwalkersws
    db.authenticate(mongouser, password=mongopass)
    col = db['%s_pilot'%site]
    pid = col.find_one({'name': pilot}, {'pilot_id': 1})
    return pid['pilot_id']

def get_users_id_by_pilot_id(site, pilot_id):
    """
    Gets all the users object id that matches the pilot id as a set
    :param site:
    :param pilot_id:
    :return:
    """
    client = MongoClient(mongoserver)
    db = client.iwalkersws
    db.authenticate(mongouser, password=mongopass)
    col = db['%s_user'%site]
    users = col.find({'user_id2': {'$regex': pilot_id + '.*'}}, {'_id': 1})

    dusers = set()
    for u in users:
        dusers.add(u['_id'])
    return dusers


def get_site_exercises_info(site, pilot, query):
    """
    Gets the exercises from a given mongo exercises table from a specific pilot
    and returns a dictionary of user_id with a list of ts and paths
    :param site:
    :param query:
    :return:
    """
    client = MongoClient(mongoserver)
    db = client.iwalkersws
    db.authenticate(mongouser, password=mongopass)
    pid = get_pilot_id(site, pilot)
    users = get_users_id_by_pilot_id(site, pid)
    col = db['%s_exercise'%site]
    exercises = col.find(query, {'path': 1, 'user_id': 1, 'ts': 1})
    dres = {}
    for ex in exercises:
        if ex['user_id'] in users:
            user = ex['user_id']
            if user in dres:
                dres[user].append((ex['ts'],convert_path(ex['path'])))
            else:
                dres[user] = [(ex['ts'],convert_path(ex['path']))]
    return dres


def get_site_exercises_variables(site, pilot, query, variables):
    """
    Gets the exercises from a given mongo exercises table from a specific pilot
    and returns a dictionary of user_id with a list of ts and a dictionary of variables

    :param site:
    :param pilot:
    :param query:
    :return:
    """
    client = MongoClient(mongoserver)
    db = client.iwalkersws
    db.authenticate(mongouser, password=mongopass)
    pid = get_pilot_id(site, pilot)
    users = get_users_id_by_pilot_id(site, pid)
    col = db['%s_exercise'%site]
    exercises = col.find(query)
    dres = {}
    for ex in exercises:
        if ex['user_id'] in users:
            user = ex['user_id']
            lvars = {}
            for var in variables:
                lvars[var] = (ex[var])
            if user in dres:
                dres[user].append((ex['ts'], lvars))
            else:
                dres[user] = [(ex['ts'], lvars)]
    return dres


if __name__ == '__main__':
    res = get_site_exercises_variables('idf',
                                  'MoSG',
                                  {'koe': '10MWT', 'd':{'$gt':0}},
                                  ["lhf_av", "rhf_av"]
                                  )
    for r in res:
        print(res[r])


