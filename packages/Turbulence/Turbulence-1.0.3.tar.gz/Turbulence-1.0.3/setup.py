from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(name='Turbulence',  # 包名
      version='1.0.3',  # 版本号
      description='Code for Turbulence Analyze',
      long_description=long_description,
      author='Li XinJUN',
      install_requires=['h5py','scipy','sympy','numpy','findiff'],
      include_package_data = True,
      package_data = {'Turbulence': ['data/dbinfo.h5','data/coefficient.tar.gz']},
      author_email='lxjproductivity@gmail.com',
      url='https://github.com/AdwardAllan',
      license='GNU License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )