import h5py 
import pyJHTDB
import numpy as np


f=h5py.File("dbinfo.h5","w")



for key,value in pyJHTDB.dbinfo.channel.items():
       f['channel'+key]=value 



for key,value in pyJHTDB.dbinfo.channel5200.items():
       f['channel5200'+key]=value 


for key,value in pyJHTDB.dbinfo.transition_bl.items():
       f['transition_bl'+key]=value 



f.close()
