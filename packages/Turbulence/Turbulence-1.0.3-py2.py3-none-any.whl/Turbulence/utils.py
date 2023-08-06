import os
# import shutil
import h5py
import pickle

import pandas as pd
# import numpy as nnp
import numpy
try:
  import cupy as np

except:
  import numpy as np
import matplotlib.pyplot as plt
import time as tt
import scipy.io as sio
# import pyJHTDB
import findiff

def getdiffcoef(order:int=1,fdorder:int=8,axes:str='x'):
  return h5py.File('/tmp/operator.h5','r')['baryctrwt-diffmat-'+str(axes)+'-r-'+str(order)+'-fd'+str(fdorder)+'.dat'][:]
def diffmy(phy:np.ndarray,forder,phydim:int):
  #phy::nz ny nx phydim
  coefy=getdiffcoef(1,forder,axes='y')[:,4:]
  offset=getdiffcoef(1,forder,axes='y')[:,:4]
  coefz=getdiffcoef(1,forder,axes='z')
  coefx=getdiffcoef(1,forder,axes='x')

  coefy2=getdiffcoef(2,forder,axes='y')[:,4:]
  offset2=getdiffcoef(2,forder,axes='y')[:,:4]
  coefz2=getdiffcoef(2,forder,axes='z')
  coefx2=getdiffcoef(2,forder,axes='x')
  #phyg phyh::nz ny nx phydim
  phyg=np.zeros((info['nx']-forder,info['ny']*2,info['nz']-forder,3*phydim))
  phyh=np.zeros((info['nx']-forder,info['ny']*2,info['nz']-forder,9*phydim))
  
  tmp=np.zeros((128,512,128,phydim))
  tmp[:,0:256,:,:]=phy[:,:,:,:]
  tmp[:,256:512,:,:]=phy[:,::-1,:,:]
  phy=tmp
  
  #循环phydim
  for dim in range(0,phydim):
    #对称提出莫伊维度
    tmp=phy[:,:,:,dim]
    #**********************************************************************#
    dy=np.zeros((128,512,128))
    for id in range(0,coefy.shape[1]):
      index=list(np.array(offset[:,2]+id,dtype=np.int).get())
      dy[:,:,:]+=tmp[:,index,:]*np.array(coefy[:,id].reshape((1,512,1)))
    
    dy2=np.zeros((128,512,128))
    for id in range(0,coefy2.shape[1]):
      index=list(np.array(offset2[:,2]+id,dtype=np.int).get())
      dy2[:,:,:]+=tmp[:,index,:]*np.array(coefy2[:,id].reshape((1,512,1)))
    ###
    phyg[:,:,:,dim*3+1]=dy[forder//2:128-forder//2,:,forder//2:128-forder//2]
    phyh[:,:,:,dim*9+4]=dy2[forder//2:128-forder//2,:,forder//2:128-forder//2]

    #**********************************************************************#
    dz=np.zeros((128-forder,512,128))
    for id in range(0,coefz.shape[0]):
      id=id-int(forder//2)
      dz[:,:,:]+=tmp[forder//2+id:128-forder//2+id,:,:]*coefz[id+forder//2]

    dz2=np.zeros((128-forder,512,128))
    for id in range(0,coefz2.shape[0]):
      id=id-int(forder//2)
      dz2[:,:,:]+=tmp[forder//2+id:128-forder//2+id,:,:]*coefz2[id+forder//2]
    ###
    phyg[:,:,:,dim*3+2]=dz[:,:,forder//2:128-forder//2]
    phyh[:,:,:,dim*9+8]=dz2[:,:,forder//2:128-forder//2]
    #**********************************************************************#
    dydz=np.zeros((128-forder,512,128))
    for id in range(0,coefz.shape[0]):
      id=id-int(forder//2)
      dydz[:,:,:]+=dy[forder//2+id:128-forder//2+id,:,:]*coefz[id+forder//2]
    
    dzdy=np.zeros((128-forder,512,128))
    for id in range(0,coefy.shape[1]):
      index=list(np.array(offset[:,2]+id,dtype=np.int).get())
      dzdy[:,:,:]+=dz[:,index,:]*np.array(coefy[:,id].reshape((1,512,1)))
    ###  
    phyh[:,:,:,dim*9+5]=dydz[:,:,forder//2:128-forder//2]
    phyh[:,:,:,dim*9+7]=dzdy[:,:,forder//2:128-forder//2]

    #**********************************************************************#
    dx=np.zeros((128,512,128-forder))
    for id in range(0,coefx.shape[0]):
      id=id-int(forder//2)
      dx[:,:,:]+=tmp[:,:,forder//2+id:128-forder//2+id]*coefx[id+forder//2]

    dx2=np.zeros((128,512,128-forder))
    for id in range(0,coefx2.shape[0]):
      id=id-int(forder//2)
      dx2[:,:,:]+=tmp[:,:,forder//2+id:128-forder//2+id]*coefx2[id+forder//2]
    ###
    phyg[:,:,:,dim*3+0]=dx[forder//2:128-forder//2,:,:]
    phyh[:,:,:,dim*9+0]=dx2[forder//2:128-forder//2,:,:]
    #**********************************************************************#
    dydx=np.zeros((128,512,128-forder))
    for id in range(0,coefx.shape[0]):
      id=id-int(forder//2)
      dydx[:,:,:]+=dy[:,:,forder//2+id:128-forder//2+id]*coefx[id+forder//2]
    
    dxdy=np.zeros((128,512,128-forder))
    for id in range(0,coefy.shape[1]):
      index=list(np.array(offset[:,2]+id,dtype=np.int).get())
      dxdy[:,:,:]+=dx[:,index,:]*np.array(coefy[:,id].reshape((1,512,1)))
    ###
    phyh[:,:,:,dim*9+3]=dydx[forder//2:128-forder//2,:,:]
    phyh[:,:,:,dim*9+1]=dxdy[forder//2:128-forder//2,:,:]

    #**********************************************************************#
    dxdz=np.zeros((128-forder,512,128-forder))
    for id in range(0,coefz.shape[0]):
      id=id-int(forder//2)
      dxdz[:,:,:]+=dx[forder//2+id:128-forder//2+id,:,:]*coefz[id+forder//2]

    dzdx=np.zeros((128-forder,512,128-forder))
    for id in range(0,coefx.shape[0]):
      id=id-int(forder//2)
      dzdx[:,:,:]+=dz[:,:,forder//2+id:128-forder//2+id]*coefx[id+forder//2]
    ###    
    phyh[:,:,:,dim*9+2]=dxdz
    phyh[:,:,:,dim*9+6]=dzdx
    #**********************************************************************#
  return phy[forder//2:128-forder//2,:,forder//2:128-forder//2,:],phyg,phyh