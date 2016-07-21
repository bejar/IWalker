"""
.. module:: ropen

ropen
*************

:Description: ropen

    

:Authors: bejar
    

:Version: 

:Created on: 29/09/2015 15:29 

"""
__author__ = 'bejar'

from Config.Private import username, password, machine
import paramiko
import os

localdir = '/home/bejar/Data/IWalker/'
remotedir = '/home/jmoreno/'
addpath = 'idf_data/output/201501/clean/'
filename = '1422374765.wlk'

if not os.path.exists(localdir+addpath):
    os.makedirs(localdir+addpath)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(machine, username=username,password=password)
sftp = ssh.open_sftp()

sftp.get(remotedir+addpath+filename, localdir+addpath+filename)



