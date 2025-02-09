#!/usr/bin/env python
#
# Code adapted from https://github.com/aspuru-guzik-group/xtb-gaussian
#
# An interface between Gaussian and xtb that takes care of Hessian
# calculations and command line arguments.
import sys
import os.path
import subprocess

# if the first argument is --log-all, then the full xtb output will be
# added to the Gaussian log file
DEBUG = False
if sys.argv[0] == '--log-all':
    DEBUG = True
    sys.argv.pop(0)

# Final 6 arguments are those passed by Gaussian.
arg_gauss = sys.argv[-6:]
# Remaining arguments are for xtb.
arg_xtb = ' '.join(sys.argv[:-6])

# First, move to the directory containing the .EIn file (the Gaussian scratch
# directory.) This is so that xtb can produce a .EOut file in the same directory.
Ein_dir, Ein = os.path.split(arg_gauss[1])
Eout_dir, Eout = os.path.split(arg_gauss[2])
Elog_dir, Elog = os.path.split(arg_gauss[3])

os.chdir(Ein_dir)
# Open input file and load parameters.
with open(Ein, 'r') as INF:
    line = INF.readline()
    natoms, deriv, icharg, multip = line.split()


# Setup redirection of xtb output. Here we throw it out instead, unless DEBUG
# is on. We do this because otherwise the Gaussian output gets way too cluttered.
msg_output = f"> {Elog} 2>&1" if DEBUG else f">/dev/null 2>{Elog}"
# Setup xtb according to run type
runtype = "--grad" if deriv < 2 else "--hess"
xtb_run = f"xtb ./{Ein} {arg_xtb} {runtype} --charge {icharg} {msg_output}"

# RUN XTB with arguments above
subprocess.call(xtb_run, shell=True)
# END of XTB run

with open(Elog, "a") as LOGF:
    LOGF.write("\n------- xtb command was ---------\n")
    LOGF.write(f"?> {xtb_run}\n")
    LOGF.write("---------------------------------\n")

    if not multip == 1:
        LOGF.write(f"WARNING: Gaussian multiplicity S={multip} is not singlet.\n")
        LOGF.write("         This is not not explicitly supported. Results are likely wrong without\n")
        LOGF.write("         an appropriate --uhf argument xtb command line!\n")

    if deriv > 2:
        # Appending to xtb gaussian formatted output
        with open(Eout, "a") as OUTP:
            # First, we fake the polarizability and the dipole derivatives, which the
            # Gaussian Manual says should be of this form,
            # Polar(I), I=1,6          3D20.12
            # DDip(I), I=1,9*NAtoms    3D20.12
            for _ in range(3 * natoms + 2):
                OUTP.write("{:20.12e}{:20.12e}{:20.12e}\n".format(0.0, 0.0, 0.0))
            
            # Now we are iterating over Hessian matrix elements. We will
            # append those to the output file in the correct format, given in
            # the Gaussian manual as

            # FFX(I), I=1,(3*NAtoms*(3*NAtoms+1))/2      3D20.12

            # That is, the lower triangular part of the Hessians only. For this we need
            # to remember which indices we have done.

            with open("hessian", "r") as HESSF:
                icol = 0
                irow = 0
                counter3 = 0
                for line in HESSF.readlines()[1:]:
                    for h in line.split():
                        if icol <= irow:
                            if counter3 == 3:
                                counter3 = 0
                                OUTP.write('\n')
                            else:
                                OUTP.write("{:20.12e}".format(h))
                            counter3+=1
                        else:
                            icol+=1
                            if icol == 3*natoms:
                                irow+=1
                                icol=0
        
        LOGF.write("             Control returned to Gaussian.\n")
        LOGF.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")