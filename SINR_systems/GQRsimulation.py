import numpy as np
from scipy import integrate
from GaussQuadrature import GQR_packet_radio,GQR_cellular_system,GQRmulti_access
import seaborn as sns
import matplotlib.pyplot as plt

################################################################################
#                               Packet radio                                   #
################################################################################

print("\n\nPACKET RADIO SIMULATION")
l = [1e-6, 5e-6, 1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 5e-2]

psuccess_6dB = []
psuccess_10dB = []
r0 = 10
R = 100
for ll in l:
    np.random.seed(0)
    psuccess_6dB.append(GQR_packet_radio(r0=r0, R=R, SIR_threshold=6, inter_density=ll, sigma=8)['success_prob'])
    psuccess_10dB.append(GQR_packet_radio(r0=r0, R=R, SIR_threshold=10, inter_density=ll, sigma=8)['success_prob'])
    print("6db, density {}, success prob {:.2f}".format(ll, psuccess_6dB[-1]))
    print("10db, density {}, success prob {:.2f}".format(ll, psuccess_10dB[-1]))

# plot
sns.set_theme(style="white", font_scale=2, palette="Dark2")
fig, ax = plt.subplots(figsize=(10,6))
ms = 10
lw = 2
ls = '--'
sns.lineplot(x=l, y=psuccess_6dB, ax=ax, label="threshold 6dB", lw=lw, marker="o", ms=ms, ls=ls)
sns.lineplot(x=l, y=psuccess_10dB, ax=ax, label="threshold 10dB", lw=lw, marker="o", ms=ms, ls=ls)
ax.set_xlabel("interference density")
ax.set_ylabel("success probability")
ax.set_xscale("log")

import os
if not os.path.exists("figures"): os.makedirs("figures")
fig.savefig("figures/GQRpacket_radio.pdf", bbox_inches='tight')


################################################################################
#                               Cellular system                                #
################################################################################
print("\n\nCELLULAR SYSTEM SIMULATION")
a = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
outage_6dB = []
outage_10dB = []
R = 0.91
R1 = R # outside of the cell
R2 = R1+2*R

for aa in a:
    np.random.seed(0)
    outage_6dB.append(GQR_cellular_system(R, SIR_threshold=6, alpha=aa, sigma=8, eta=4, R1=R1, R2=R2)['failure_prob'])
    outage_10dB.append(GQR_cellular_system(R, SIR_threshold=10, alpha=aa, sigma=8, eta=4, R1=R1, R2=R2)['failure_prob'])
    print("6db, prob alpha {}, outage prob {:.2f}".format(aa, outage_6dB[-1]))
    print("10db, prob alpha {}, outage prob {:.2f}".format(aa, outage_6dB[-1]))

fig, ax = plt.subplots(figsize=(10,6))
sns.lineplot(x=a, y=outage_6dB, ax=ax, label="threshold 6dB", lw=lw, marker="o", ms=ms, ls=ls)
sns.lineplot(x=a, y=outage_10dB, ax=ax, label="threshold 10dB", lw=lw, marker="o", ms=ms, ls=ls)

ax.set_xlabel("interference probability")
ax.set_ylabel("outage probability")
fig.savefig("figures/GQRcellular_system.pdf", bbox_inches='tight')

################################################################################
#                               Multi-access                                   #
################################################################################
print("\n\nMULTI-ACCESS SIMULATION")
G = [2+i*5 for i in range(0,20)]
throughput_6dB = []
throughput_10dB = []

R = 1
for gg in G:
    np.random.seed(0)
    throughput_6dB.append(GQRmulti_access(R, SIR_threshold=6, G=gg, sigma=8)['success_prob'])
    throughput_10dB.append(GQRmulti_access(R, SIR_threshold=10, G=gg, sigma=8)['success_prob'])
    print("6db, G {}, throughput {:.2f}".format(gg, throughput_6dB[-1]))
    print("10db, G {}, throughput {:.2f}".format(gg, throughput_6dB[-1]))

fig, ax = plt.subplots(figsize=(10,6))
sns.lineplot(x=G, y=throughput_6dB, ax=ax, label="threshold 6dB", lw=lw, marker="o", ms=ms, ls=ls)
sns.lineplot(x=G, y=throughput_10dB, ax=ax, label="threshold 10dB", lw=lw, marker="o", ms=ms, ls=ls)

ax.set_xlabel("Average number of transmissions per slot")
ax.set_ylabel("throughput")
fig.savefig("figures/GQRmulti_access.pdf", bbox_inches='tight')

