
import setuptools
from setuptools import setup, find_packages
import codecs
import os
with open("Readme.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ARAMBHML',
    version='0.0.2',
    description='An Auto ML framework that solves Classification Tasks',
    author= 'Amartya Bhattacharya,Rupam Kumar Roy',
   
    long_description = long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=['auto ml python', 'classification problem', 'machine learning'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
   # python_requires='>=3.6',
  #  py_modules=['ARAMBHML'],
  #  package_dir={'':'src'},
    install_requires = [
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'sklearn-pandas',
        'xgboost',
        'plotly',
        'plotly-express'
    ]
)
