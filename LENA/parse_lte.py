
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = np.loadtxt('../DlPdcpStats.txt', skiprows=1);

cell1 = data[data[:, 2] == 1, :]
cell2 = data[data[:, 2] == 2, :]

sns.set_theme(style="white", font_scale=2, palette="Dark2")
fig, ax = plt.subplots(figsize=(10,6))
ax.errorbar(cell1[:, 0], cell1[:, 10], cell1[:, 11], fmt='o', label="cell 1")
ax.errorbar(cell2[:, 0], cell2[:, 10], cell2[:, 11], fmt='o', label="cell 2")
ax.set_xlabel("time (s)")
ax.ylim(0)
fig.savefig("CELL.pdf", bbox_inches='tight')
