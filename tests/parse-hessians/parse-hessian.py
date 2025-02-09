#%%
import itertools
import numpy as np
import cclib
#%%
natoms = 16

def parseHess(hessfile,natoms):
    """
    Returns Hessian in lower triangular form (1D array)
    from a Freq iop(7/33)=1 Gaussian out file
    """
    with open(hessfile) as file:
        lines = list(
            itertools.takewhile(
                lambda line: 'Final forces' not in line, 
                itertools.dropwhile(
                lambda line: 'Force constants' not in line, file
                )
            )
        )
    lines = [line.strip("\n").split()[1:] for line in lines][1:]
    for idx in np.cumsum([0]+[i+1 for i in range(3*natoms,0,-5)])[:-1][::-1]: del lines[idx]
    lines = np.array([li.replace("D","E") for line in lines for li in line]).astype(np.float64)
    return lines

Htril_new = parseHess("da-1_2_freq.out",natoms)
Htril_old = parseHess("da-1_2_OLD.out",natoms)

#%%

H_new = np.tril(Htril_new) + np.tril(Htril_new, -1).T
eig_new = np.sort(np.linalg.eigh(H_new)[0])

H_old = np.tril(Htril_old) + np.tril(Htril_old, -1).T
eig_old = np.sort(np.linalg.eigh(H_old)[0])

print(Htril_new)
print(Htril_old)
print(eig_new)
print(eig_old)

assert H_new.all() == H_old.all()

#%%