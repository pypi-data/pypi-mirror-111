########################################################################
#
#  Copyright 2021 Harbin Institute of Technology Shenzhen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Contact: lxjproductivity@gmail.com
#
########################################################################

"""
Python tools and wrappers 
.. code:: python
    >>> from pyJHTDB import test
    >>> test()
"""

import os
import os.path
import sys
import numpy as np
import ctypes
import platform
# 包版本管理
from pkg_resources import get_distribution, DistributionNotFound

try:
    _dist = get_distribution('Turbulence')
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, 'Turbulence')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:
    __version__ = _dist.version
# 信息构建
auth_token = 'com.outlook.lxjproductivity-74623636'
homefolder = os.path.expanduser('~')
lib_folder = os.path.join(homefolder, '.config/', 'Turbulence/')
version_info = "20210703.0"
version = str(version_info)

# check if .config/JHTDB folder exists, create it if not
if os.path.isdir(lib_folder):
   if os.path.exists(os.path.join(lib_folder, 'auth_token.txt')):
       auth_token = str(open(os.path.join(lib_folder, 'auth_token.txt'), 'r').readline().split()[0])
   else:
       open(os.path.join(lib_folder, 'auth_token.txt'), 'w').write(auth_token)
else:
   os.mkdir(lib_folder)
   open(os.path.join(lib_folder, 'auth_token.txt'), 'w').write(auth_token)
#外部包导入
try:
    import h5py
    found_h5py = True
except ImportError:
    found_h5py = False
    print('h5py not found. cutout functionality not available.')

try:
    import matplotlib
    found_matplotlib = True
except ImportError:
    found_matplotlib = False
    print('matplotlib not found. plotting functionality not available.')

try:
    import scipy
    found_scipy = True
except ImportError:
    found_scipy = False
    print('scipy not found. not all interpolation functionality available')
# 内部相对包导入
from .api import *
from .test import *
from .statistics import *
from .utils import *