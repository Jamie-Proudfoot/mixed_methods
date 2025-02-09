#%%

import numpy as np
import os

#%%

new = open("newhess.txt","r")
new_lines = new.readlines()
block = np.array([line.split() for line in new_lines]).astype(float).flatten()
x = len(block)
r1 = 0.5 * (np.sqrt(8 * x + 1) - 1)
r2 = 0.5 * (-np.sqrt(8 * x + 1) - 1)
dim = int(max(r1, r2))
mat = np.empty(shape=(dim, dim))
mat[np.tril_indices_from(mat)] = block
hess = np.tril(mat)+np.tril(mat,-1).T
eig = np.linalg.eigh(hess)[0]
print(np.round(eig,9))

#%%

new = open("oldhess.txt","r")
new_lines = new.readlines()
block = np.array([line.split() for line in new_lines]).astype(float).flatten()
x = len(block)
r1 = 0.5 * (np.sqrt(8 * x + 1) - 1)
r2 = 0.5 * (-np.sqrt(8 * x + 1) - 1)
dim = int(max(r1, r2))
mat = np.empty(shape=(dim, dim))
mat[np.tril_indices_from(mat)] = block
hess = np.tril(mat)+np.tril(mat,-1).T
eig = np.linalg.eigh(hess)[0]
print(np.round(eig,9))

#%%

# CARTESIAN HESSIAN

new = open("newhess_cart.txt","r")
new_lines = new.readlines()
block = [line.split() for line in new_lines]
block = np.array([li for line in block for li in line]).astype(float)
x = len(block)
r1 = 0.5 * (np.sqrt(8 * x + 1) - 1)
r2 = 0.5 * (-np.sqrt(8 * x + 1) - 1)
dim = int(max(r1, r2))
mat = np.empty(shape=(dim, dim))
mat[np.tril_indices_from(mat)] = block
hess = np.tril(mat)+np.tril(mat,-1).T
eig = np.linalg.eigh(hess)[0]
print(np.round(eig,9))

#%%

# CARTESIAN HESSIAN

new = open("newhess_EOu_cart.txt","r")
new_lines = new.readlines()
block = [line.split() for line in new_lines]
block = np.array([li for line in block for li in line]).astype(float)
x = len(block)
r1 = 0.5 * (np.sqrt(8 * x + 1) - 1)
r2 = 0.5 * (-np.sqrt(8 * x + 1) - 1)
dim = int(max(r1, r2))
mat = np.empty(shape=(dim, dim))
mat[np.tril_indices_from(mat)] = block
hess = np.tril(mat)+np.tril(mat,-1).T
eig = np.linalg.eigh(hess)[0]
print(np.round(eig,9))

#%%