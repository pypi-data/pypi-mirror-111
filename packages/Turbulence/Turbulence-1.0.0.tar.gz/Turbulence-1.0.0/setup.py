from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(name='Turbulence',  # 包名
      version='1.0.0',  # 版本号
      description='Code for Turbulence Analyze',
      long_description=long_description,
      author='Li XinJUN',
      author_email='lxjproductivity@gmail.com',
      url='https://github.com/AdwardAllan',
      install_requires=[],
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