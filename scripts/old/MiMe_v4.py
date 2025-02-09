#!/usr/bin/env python3

#%%

########## PYTHON IMPORTS ##########

import sys
import os.path
import subprocess
import numpy as np
import argparse
from shutil import which
import cclib
import time

########## PYTHON IMPORTS ##########

#%%

########## READ IN FROM EXTERNAL INPUT FILE ##########

# Parse command line arguments passed to MixedHess
parser = argparse.ArgumentParser(
    description="MiMe (Mixed Methods) Allows Gaussian to use \
    mixed levels of theory for 0th, 1st and 2nd derivatives of \
    energy, via the 'External' keyword. Currently supports one \
    level of theory for Energy and Forces, and another for Hessians.\
    There is a non-negligible overhead for the IO operations involved \
    therefore this method is not recommended for calculations involving \
    only low levels of theory (e.g. MM/SQM methods) where the calculation \
    times are similar to the IO operations.")
# These arguments define the levels of theory.
parser.add_argument("-E", "--spelevel", type=str,
    help="level of theory for energy", default="")
parser.add_argument("-F", "--gradlevel", type=str,
    help="level of theory for force", default="")
parser.add_argument("-EF", "--eflevel", type=str,
    help="level of theory for energy and forces")
parser.add_argument("-H", "--hesslevel", type=str,
    help="level of theory for hessian", default="")
# These arguments specify the computational requirements
parser.add_argument("-c", "--nprocshared", type=str,
    help="number of cpu cores to be used", default="12")
parser.add_argument("-m", "--memory", type=str,
    help="amount of dynamic memory to be used", default="48GB")
# Remaining (6) arguments are supplied by Gaussian.
parser.add_argument("gauss", nargs=argparse.REMAINDER,
    help="additional arguments provided by Gaussian")
args = vars(parser.parse_args())

# If no arguments passed
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(0)

# Extract arguments relevant to mixedhess code
spelevel = args['spelevel']
gradlevel = args['gradlevel']
if 'eflevel' in args:
    spelevel = gradlevel = args['eflevel']
hesslevel = args['hesslevel']
nprocshared = args['nprocshared']
mem = args['memory']

# Gaussian passes the final 6 arguments
arg_gauss = sys.argv[-6:]
# Preceding arguments are for MixedHess
arg_mime = ' '.join(sys.argv[:-6])

# Move to the directory containing the .EIn file
# this should be the Gaussian scratch directory.
# This is so that MixedHess code can produce a
# .EOu file in the same directory.

# Extract the 6 arguments provided by Gaussian
# layer InputFile OutputFile MsgFile FChkFile MatElFile
Ein_dir, Ein = os.path.split(args['gauss'][1])
Eout_dir, Eout = os.path.split(args['gauss'][2])
Elog_dir, Elog = os.path.split(args['gauss'][3])

# Code for the current Gaussian job
# arbitrarily created by Gaussian
# takes the form 'Gau-012345'
gau_name = Ein.split('.')[0]

# Enter the directory for computation
# this should be the Gaussian scratch directory
os.chdir(Ein_dir)

# Open input file and load parameters.
INP = open(Ein,"r")
lines = INP.readlines()

# Extract header information
natoms, deriv, charge, spin = map(int, lines[0].split())

# Extract geometry specification
geom = ''
# each line contains: atomicNo  x  y  z  MM-charge
atoms = np.array([li.split() for li in lines][1:natoms+1])
# must convert from Bohr to Angstrom XYZ units
# BOHR_ANGST=0.52917721092
# (conversion ref: Gaussian - Constants)
# xyz = atoms[:,1:-1].astype(float)*BOHR_ANGST
# this can be done with units=au in gjf files
xyz = atoms[:,1:-1].astype(float)
for i in range(natoms):
    li = np.append(atoms[i,0],xyz[i])
    geom += ' '.join(li)+'\n'

########## READ IN FROM EXTERNAL INPUT FILE ##########

#%%

########## WRITE TO GAUSSIAN INPUT FILES ##########


# Job specifications for SPE, FORCE and FREQ calculations
# units=au specifies that coordinates are in bohr

spejob = "#"+" "+spelevel+" "+"units=au "
gradjob = "#"+" "+gradlevel+" "+"force units=au "
hessjob = "#"+" "+hesslevel+" "+"freq=(noraman,noprintnm) units=au "

# Redundancy logic
# to avoid repeated calculations
# at the same level of theory
# FREQ contains hess, grads and spe
# FORCE contains grads and spe
# SPE contains spe only

runspe = runforce = runfreq = False

if deriv == 2:
    runfreq = True
    if hesslevel != gradlevel:
        runforce = True
    elif hesslevel != spelevel:
        runspe = True
elif deriv == 1:
    runforce = True
    if gradlevel != spelevel:
        runspe = True
elif deriv == 0:
    runspe = True


# CHANGE THIS WHEN NECESSARY
runforce = True

print("")
print(f"deriv: {deriv}")
print("")
print(f"spelevel: {spelevel}")
print(f"gradlevel: {gradlevel}")
print(f"hesslevel: {hesslevel}")
print("")
print(f"runspe: {runspe}")
print(f"runforce: {runforce}")
print(f"runfreq: {runfreq}")

# Write SPE job to a temporary gjf file
spe_infile = gau_name+"_E.gjf"
spe_outfile = gau_name+"_E.out"
if runspe:
    with open(spe_infile,"w") as SPE:
        SPE.write("%nprocshared="+nprocshared+"\n")
        SPE.write("%mem="+mem+"\n")
        SPE.write(spejob+"\n")
        SPE.write("\n"+"SPE part at "+spelevel+"\n\n")
        SPE.write(str(charge)+"  "+str(spin)+"\n")
        SPE.write(geom)
        SPE.write("\n")

# Write FORCE job to a temporary gjf file
grad_infile = gau_name+"_F.gjf"
grad_outfile = gau_name+"_F.out"
if runforce:
    with open(grad_infile,"w") as GRAD:
        GRAD.write("%nprocshared="+nprocshared+"\n")
        GRAD.write("%mem="+mem+"\n")
        GRAD.write(gradjob+"\n")
        GRAD.write("\n"+"GRAD part at "+gradlevel+"\n\n")
        GRAD.write(str(charge)+"  "+str(spin)+"\n")
        GRAD.write(geom)
        GRAD.write("\n")

# Write FREQ job to a temporary gjf file
freq_infile = gau_name+"_H.gjf"
freq_outfile = gau_name+"_H.out"
freq_chkfile = gau_name+"_H.chk"
freq_fchkfile = gau_name+"_H.fchk"
if runfreq:
    with open(freq_infile,"w") as FREQ:
        FREQ.write("%chk="+freq_chkfile+"\n")
        FREQ.write("%nprocshared="+nprocshared+"\n")
        FREQ.write("%mem="+mem+"\n")
        FREQ.write(hessjob+"\n")
        FREQ.write("\n"+"FREQ part at "+hesslevel+"\n\n")
        FREQ.write(str(charge)+"  "+str(spin)+"\n")
        FREQ.write(geom)
        FREQ.write("\n")

########## WRITE TO GAUSSIAN INPUT FILES ##########

#%%

########## GAUSSIAN CALCULATIONS ###########

# Find path to Gaussian
gaussian = which("g16")
if not gaussian: gaussian = which("g13")
if not gaussian: gaussian = which("g09")
if not gaussian: raise FileNotFoundError(
    "Gaussian could not be found")
formchk = which("formchk")

print("\nRunning Gaussian ...")
# Run Gaussian SPE calculations (in Gaussian Scratch)
if runspe:
    spe_run = gaussian+" "+spe_infile+" "+spe_outfile
    subprocess.run(spe_run, shell=True)
# Run Gaussian FORCE calculations (in Gaussian Scratch)
if runforce:
    grad_run = gaussian+" "+grad_infile+" "+grad_outfile
    subprocess.run(grad_run, shell=True)
# Run Gaussian FREQ calculations (in Gaussian Scratch)
if runfreq:
    freq_run = gaussian+" "+freq_infile+" "+freq_outfile
    subprocess.run(freq_run, shell=True)
    subprocess.run(formchk+" "+freq_chkfile, shell=True)

########## GAUSSIAN CALCULATIONS ##########

#%%

########### EXTRACT DATA FROM GAUSSIAN CALCULATIONS ##########

print("\nParsing files ...")

# Redundancy logic
# to avoid repeat calculations
# at the same level of theory
spefile = spe_outfile
gradfile = grad_outfile
hessfile = freq_outfile

if not runspe and runforce:
    # not running spe and running force
    # implies spelevel == forcelevel
    spefile = gradfile
if not runspe and not runforce:
    # not running spe or force
    # implies spelevel == forcelevel == hesslevel
    spefile = gradfile = hessfile
if runspe and not runforce:
    # not running force and running spe
    # implies forcelevel == hesslevel
    gradfile = hessfile

# CHANGE THIS LATER
gradfile = grad_outfile

print(f"SPE file: {spefile}")
if deriv >= 1:
    print(f"FORCE file: {gradfile}")
if deriv >= 2:
    print(f"HESS file: {hessfile}")

# Parse SPE file
parser = cclib.io.ccopen(spefile)
data = parser.parse()
# Extract Energy
# must convert from eV to Hartree
EV_HARTREE = 0.03674932379085202
# (conversion ref: cclib.parser.utils)
E = data.scfenergies*EV_HARTREE
# Extract Dipole moment
D = data.moments[1]
data = 0
if deriv >= 1:
    # Parse FORCE file
    parser = cclib.io.ccopen(gradfile)
    # Extract Forces
    F = parser.parse().grads[-1]
if deriv == 2:
    # Parse FREQ formatted checkpoint file
    parser = cclib.io.ccopen(freq_fchkfile)
    # Extract Hessian
    H = parser.parse().hessian
    # Write to lower triangular form
    Htril = H[np.tril_indices_from(H)]


# Delete Gaussian files
#if runspe:
#    subprocess.run("rm"+" "+spe_infile, shell=True)
#    subprocess.run("rm"+" "+spe_outfile, shell=True)
#if runforce:
#    subprocess.run("rm"+" "+grad_infile, shell=True)
#    subprocess.run("rm"+" "+grad_outfile, shell=True)
#if runfreq:
#    subprocess.run("rm"+" "+freq_infile, shell=True)
#    subprocess.run("rm"+" "+freq_outfile, shell=True)
#    subprocess.run("rm"+" "+freq_chkfile, shell=True)
#    subprocess.run("rm"+" "+freq_fchkfile, shell=True)

########### EXTRACT DATA FROM GAUSSIAN CALCULATIONS ##########

#%%

########## WRITE TO MSG FILE (GAUSSIAN OUT FILE) ##########

mime_run = "MiMe"+" "+arg_mime
with open(Elog, "w") as LOGF:
    LOGF.write("\n--------------------------------------------------\n")
    if runspe:
        LOGF.write(f"\nEnergy calculation at {spelevel}\n")
    if deriv >= 1 and runforce:
        LOGF.write(f"Force calculation at {gradlevel}\n")
    if deriv == 2:
        LOGF.write(f"Hessian calculation at {hesslevel}\n")


#print("")
#print(f"E: {E}")
#print("")
#print(f"F: {F}")
#print(f"shape: {F.shape}")
#print("")
#print(f"H: {H}")
#print(f"shape: {H.shape}")
#print("")

########## WRITE TO MSG FILE (GAUSSIAN OUT FILE) ##########

#%%

########## WRITE TO EXTERNAL OUTPUT FILE ##########

with open(Eout,"w") as OUTP:
    # Energy, Dipole moment (xyz)
    # E, Dip(I), I=1,3 	  	                 4D20.12
    ED = np.append(E,D)
    OUTP.write(str("{:20.12e}"*4).format(*ED)+"\n")

    # Gradient on atoms (xyz) (N.B. these are -ve of Forces)
    # FX(J,I), J=1,3; I=1,NAtoms 	         3D20.12
    if deriv >= 1:
        for row in -F:
            OUTP.write(str("{:20.12e}"*3).format(*row)+"\n")

    # Arbitrary Polrizability and Dipole-gradient values (set to 0.0)
    # Polar(I), I=1,6                            3D20.12
    # DDip(I), I=1,9*NAtoms                      3D20.12
    for i in range(3*natoms+2):
        OUTP.write(str("{:20.12e}"*3).format(0.0, 0.0, 0.0)+"\n")

    # Hessian (force constant) values
    # FFX(I), I=1,(3*NAtoms*(3*NAtoms+1))/2      3D20.12
    if deriv == 2:
        for i in range(0,len(Htril),3):
            row = Htril[i:i+3]
            OUTP.write(str("{:20.12e}"*3).format(*row)+"\n")

########## WRITE TO EXTERNAL OUTPUT FILE ##########

#%%
