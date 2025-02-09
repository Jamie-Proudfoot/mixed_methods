#%%
import numpy as np
import cclib
import itertools
#%%

def parseHess(hessfile):
    """
    Returns Internal Hessian in lower triangular form (1D array)
    from a Freq=IntModes fchk file
    """
    with open(hessfile) as file:
        lines = list(
            itertools.takewhile(
            lambda line: 'Mulliken Charges' not in line, 
            itertools.dropwhile(
            lambda line: 'Internal Force Constants' not in line, file)))
    lines = [line.strip("\n").split() for line in lines][1:]
    lines = np.array([li for line in lines for li in line]).astype(np.float64)
    return lines

#%%

gau_name = "Gau-627631"
gau_EFC = gau_name+".EFC"

spefile = gau_name+"_F.out"
gradfile = gau_name+"_F.fchk"
hessfile = gau_name+"_H.fchk"

#%%

energy = cclib.io.ccopen(gradfile).parse().scfenergies[-1]
energy *= 0.03674932379085202
dipole = cclib.io.ccopen(spefile).parse().moments[1]
grads = cclib.io.ccopen(gradfile).parse().grads

inthess = parseHess(hessfile)

print(energy)
print()
print(dipole)
print()
print(grads.shape)
print()
print(inthess.shape)

#%%

# def text_find(pattern, lines):
#     """
#     Find first occurence of pattern (string)
#     within the list of lines (list of strings)
#     """
#     for n, line in enumerate(lines): 
#         if pattern in line: return n

# def text_replace(lines,start,end,text):
#     s = text_find(start, lines)
#     e = text_find(end, lines)
#     lines[s:e+1] = text

# def text_write(file_name,start,end,text):
#     lines = open(file_name, 'r').readlines()
#     text_replace(lines,start,end,text)
#     out = open(file_name, 'w')
#     out.writelines(lines)
#     out.close()

# E_text = ["Grdnt Energy"+" "*31+"R"+" "*6+"{:20.15E}".format(energy)+"\n"]
# text_write(gau_EFC,"Grdnt Energy","Grdnt Energy",E_text)

#%%

# APPENDING TO FORCE FCHK FILE

with open(hessfile) as file:
    hesslines = list(
        itertools.takewhile(
        lambda line: 'Mulliken Charges' not in line, 
        itertools.dropwhile(
        lambda line: 'Internal Force Constants' not in line, file)))
    
with open(gradfile,"r") as fchkfile:
    fchklines = fchkfile.readlines()
    fchklines = fchklines[:-2]+hesslines+fchklines[-2:]

with open(gradfile,"w") as outfile:
    outfile.writelines(fchklines)

#%%