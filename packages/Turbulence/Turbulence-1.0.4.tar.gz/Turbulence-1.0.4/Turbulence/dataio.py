import os
import h5py
import pickle
import numpy
import scipy.io as sio



class dataio(object):
  def SavePkl(path,data):
    f=open(path,'wb')
    pickle.dump(data,f)
    f.close()
  def LoadPkl(path):
    f=open(path,'rb')
    data=pickle.load(f)
    f.close()
    return data
  def SaveHDF5(path:str,data:dict):
    f=h5py.File(path,'w')
    for key,value in data.items():
      f[key] = value 

    f.close()
  def LoadHDF5(path) -> dict:
    f=h5py.File(path,'r')
    tmp={}
    for key in f.keys():
      tmp[key]=f[key][()]
    f.close()
    return tmp
  def SaveMAT(path:str,data:dict):
    sio.savemat(path,data)
  def LoadMAT(path):
    return sio.loadmat(path)


  def IO(path:str,data:dict,token='I',format='pkl'):
    if token=='I':
      if format=='pkl':
        return LoadPkl(path)
      elif format=='mat':
        return LoadMAT(path)
      elif format=='h5':
        return LoadHDF5(path)
    elif token=='O':
      if format=='pkl':
        SavePkl(path,data)
      elif format=='mat':
        SaveMAT(path,data)
      elif format=='h5':
        SaveHDF5(path,data)
      return None



