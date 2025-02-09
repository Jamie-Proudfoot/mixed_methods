#%%
import numpy as np

#%%

A = np.random.randn(5,5)
B = A.T@A

def compress(B):
    return B[np.tril_indices_from(B)]

def decompress(A):
    x = int(0.5*(-1+np.sqrt(1+8*len(A))))
    B = np.zeros((x,x))
    B[np.tril_indices(x)] = A
    B = np.tril(B) + np.triu(B.T,1)
    return B

#%%
print(B)
C=compress(B)
print(C)
print(decompress(C))
# %%
