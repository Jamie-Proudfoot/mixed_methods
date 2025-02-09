#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
#%%
filename = "Catalysts-20.csv"
name = filename.split(".")[0]
df = pd.read_csv(filename)
#%%
sns.set_theme()
#%%
x = np.arange(len(df["name"]))
ax = plt.subplot(111)
ax.bar(x-0.1,df["steps(opt=calcfc)"], width=0.2, color='b', align='center', label="opt=calcfc")
ax.bar(x+0.1,df["steps(opt)"], width=0.2, color='g', align='center', label="opt")
ax.set_xticks(x)
ax.set_xticklabels(df["name"])
plt.xticks(rotation=80)
ax.set_ylabel("Steps")
ax.legend(loc="upper left")
fig = ax.figure
fig.savefig(f"{name}_steps.png", dpi=1000, bbox_inches="tight")
#%%
x = np.arange(len(df["name"]))
ax = plt.subplot(111)
ax.bar(x-0.2,df["time(opt=calcfc)"], width=0.2, color='b', align='center', label="opt=calcfc")
ax.bar(x,df["time(opt)"], width=0.2, color='g', align='center', label="opt")
ax.bar(x+0.2,df["time(freq)"], width=0.2, color='orange', align='center', label="freq")
ax.set_xticks(x)
ax.set_xticklabels(df["name"])
plt.xticks(rotation=80)
ax.set_ylabel("CPU time / s")
ax.legend(loc="upper right")
fig = ax.figure
fig.savefig(f"{name}_time.png", dpi=1000, bbox_inches="tight")
#%%
x = np.arange(len(df["name"]))
ax = plt.subplot(111)
ax.bar(x,df["dG"]*627.509, width=0.4, color='red', align='center')
ax.set_xticks(x)
ax.set_xticklabels(df["name"])
plt.xticks(rotation=80)
ax.set_ylabel("ΔG / kcal mol$^{-1}$")
# ax.set_ylim(0,16)
fig = ax.figure
fig.savefig(f"{name}_dG.png", dpi=1000, bbox_inches="tight")
#%%
x = np.arange(len(df["name"]))
ax = plt.subplot(111)
ax.bar(x,df["RMSD"], width=0.4, color='brown', align='center')
ax.set_xticks(x)
ax.set_xticklabels(df["name"])
plt.xticks(rotation=80)
ax.set_ylabel("Heavy atom RMSD / Å")
# ax.set_ylim(0,16)
fig = ax.figure
fig.savefig(f"{name}_rmsd.png", dpi=1000, bbox_inches="tight")
#%%