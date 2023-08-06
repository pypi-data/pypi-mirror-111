import os
# import shutil
import h5py
import pickle

import pandas as pd
# import numpy as nnp
import numpy
import cupy as np
import matplotlib.pyplot as plt
import time as tt
import scipy.io as sio
# import pyJHTDB



def EqDissipation(u:np.ndarray,ug:np.ndarray,uh:np.ndarray,ph:np.ndarray,UHM,UGM) -> np.ndarray:
  v=u[:,:,1].reshape((info['ny']*2,-1,1,1))# v->flux
  EQ=np.zeros((8,info['ny']*2,3,3))
  EQ[0,...]=sym(np.mean(np.einsum('...il,...kl -> ...ik',ug,ph),axis=1))
  EQ[1,...]=sym(info['nu']*np.mean(np.einsum('...ils,...kls -> ...ik',uh,uh),axis=1))
  EQ[2,...]=-info['nu']*np.mean(np.einsum('...il,...kl -> ...ik',ug,ug),axis=1)
  EQ[3,...]=np.mean(np.einsum('...il,...kl -> ...ik',ug,ug)*v,axis=1)
  EQ[4,...]=sym(np.mean(np.einsum('...il,...ks,...sl -> ...ik',ug,ug,UGM),axis=1)) 
  EQ[5,...]=sym(np.mean(np.einsum('...il,...sl,...ks -> ...ik',ug,ug,UGM),axis=1))
  EQ[6,...]=sym(np.mean(np.einsum('...il,...sl,...ks -> ...ik',ug,ug,ug),axis=1))
  EQ[7,...]=sym(np.mean(np.einsum('...s,...il,...kls -> ...ik',u,ug,UHM),axis=1)) 
  return EQ


