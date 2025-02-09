#%%

import numpy as np
import os

#%%


# Code to test rotation-translation of Cartesian geometries
# 1. Create RotTR matrix
# 2. Apply RotTR matrix to geometry

natoms=16

BOHR_ANGST = 0.52917721092

input = open("input.txt","r")
in_lines = input.readlines()
in_geom = np.array([line.strip('\n').split()[1:] for line in in_lines]).astype(float)
print(in_geom)

standard = open("standard.txt","r")
st_lines = standard.readlines()
st_lines = [line.strip('\n').split() for line in st_lines]
st_geom = np.array([li for line in st_lines for li in line]).astype(float).reshape(natoms,3)

rottr = open("RotTr.txt","r")
rt_lines = rottr.readlines()
rt_lines = [line.strip('\n').split() for line in rt_lines]
RotTr = np.array([li for line in rt_lines for li in line]).astype(float).reshape(4,3)

Tr = RotTr[-1]
Rot = RotTr[:-1]

#%%

(st_geom@Rot+Tr)*BOHR_ANGST

#%%