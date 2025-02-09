#%%
import sys
import os.path
import subprocess
import numpy as np
#%%

def writelowerT(filename, M):
    with open(filename,"a") as f:
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                if j <= i: f.write("{:20.12e}".format(M[i][j]))
            f.write("\n")

#%%

# START OF GAUSSIAN -- uncomment
# # Last 6 arguments are from Gaussian.
# arg_gauss = sys.argv[-6:]
# # Remaining arguments are for HessML.
# arg_ml = ' '.join(sys.argv[:-6])

# # Move to the directory containing the .EIn file (the Gaussian scratch directory.) 
# # This is so that HessML can produce a .EOut file in the same directory.
# Ein, Ein_dir = os.path.split(arg_gauss[1])
# Eout, Eout_dir = os.path.split(arg_gauss[2])
# Elog, Elog_dir = os.path.split(arg_gauss[3])

# os.chdir(Ein_dir)
# # Open input file and load parameters.
# with open(Ein, 'r') as INF:
#     line = INF.readline()
#     natoms, deriv, icharg, multip = line.split()
# END OF GAUSSIAN -- uncomment

natoms = 3
Eout = "Test.EOut" # TEST file name

A = np.random.randn(3*natoms,3*natoms)
H = A.T@A

# writelowerT(Eout,H)

with open(Eout,"a") as OUTP:
    #### TODO -- extract Energy, Dipole and atom grads from EIn file
    # E, Dip(I), I=1,3 	  	            4D20.12
    # FX(J,I), J=1,3; I=1,NAtoms 	  	3D20.12
    #### TODO -- extract Energy, Dipole and atom grads from EIn file 

    # Arbitrary Polrizability and Dipole-gradient values
    # Polar(I), I=1,6          3D20.12
    # DDip(I), I=1,9*NAtoms    3D20.12
    for _ in range(3*natoms+2):
        OUTP.write("{:20.12e}{:20.12e}{:20.12e}\n".format(0.0, 0.0, 0.0))
    # Hessian (force constant) values
    # FFX(I), I=1,(3*NAtoms*(3*NAtoms+1))/2      3D20.12     
    for i in range(H.shape[0]):
        OUTP.write("\n")
        for j in range(H.shape[1]):
            if j <= i: OUTP.write("{:20.12e}".format(H[i][j]))

#%%