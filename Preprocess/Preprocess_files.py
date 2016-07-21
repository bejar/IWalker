"""
.. module:: Preprocess_files

Preprocess_files
*************

:Description: Preprocess_files

    Preprocessing MADRID files to have the same format as FSL

:Authors: bejar
    

:Version: 

:Created on: 19/07/2016 8:54 

"""

from Config.Constants import odatapath,  datasets2o, datasets2, datasetso, datasets
import os

__author__ = 'bejar'
header = 'lhfx,lhfy,lhfz,rhfx,rhfy,rhfz,lnf,rnf,acc,magn,gyro,hbl,hbr,epx,epy,epo,ls,rs\n'

for ds, pds in zip(datasetso,datasets):
    print(odatapath+ds)
    lfiles = os.listdir(odatapath+ds)


    for fl in lfiles:
        print(fl.split('.'))
        ext = fl.split('.')[1]

        if ext == 'csv':
            fw = open(odatapath+pds+fl.split('.')[0]+'.csv','w')
            fw.write(header)
            fr = open(odatapath+ds+fl,'r')
            for line in fr:
                fw.write(line)
            fw.close()
            fr.close()

