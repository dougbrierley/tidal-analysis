from PyAstronomy import pyasl

import datetime

import numpy as np

import matplotlib.pyplot as plt

import pandas as pd

import scipy.io


# Define names of the headers of the data
names = ['node','longitude', 'latitude', 'depth']
nodes = pd.read_csv("new_model/fort.14_nodes",
    names=names,
    header=0,
    skipinitialspace=True, # Skip initial space after the delimiter
    delim_whitespace=True, #White space is the delimiter
    skiprows=0,
    nrows= 5200,
)

with open("new_model/fort.14_land_boundaries") as f:
    lines = f.readlines()
    for x in lines:
        

# land_boundary = 
# myfile = open("new_model/fort.14", "rt") # open lorem.txt for reading text
# contents = myfile.read()         # read the entire file to string
# myfile.close()                   # close the file
# print(contents)                  # print string contents