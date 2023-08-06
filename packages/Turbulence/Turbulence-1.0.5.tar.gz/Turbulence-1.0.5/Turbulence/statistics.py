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

def BasicStatistics(phy:np.ndarray,phydim) -> np.ndarray:
  phys=np.zeros((512,5*phydim))

  phys[:,0:phydim]=meanmy(phy**2)
  phys[:,phydim:2*phydim]=meanmy(phy**3)
  phys[:,2*phydim:3*phydim]=meanmy(phy**4)
  phys[:,3*phydim:4*phydim]=meanmy(phy**5)
  phys[:,4*phydim:5*phydim]=meanmy(phy**6)
  
  return phys 