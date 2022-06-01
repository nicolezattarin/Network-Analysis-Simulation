import numpy as np
from scipy import integrate
from GaussQuadrature import GQR_packet_radio,GQR_cellular_system,GQRmulti_access
import seaborn as sns
import matplotlib.pyplot as plt

################################################################################
#                               Packet radio                                   #
################################################################################

# print("\n\nPACKET RADIO SIMULATION")
# l = [1e-6, 5e-6, 1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 5e-2]

# psuccess_6dB = []
# psuccess_10dB = []
# r0 = 10
# R = 100
# for ll in l:
#     np.random.seed(0)
#     psuccess_6dB.append(GQR_packet_radio(r0=r0, R=R, SIR_threshold=6, inter_density=ll, sigma=8)['success_prob'])
#     psuccess_10dB.append(GQR_packet_radio(r0=r0, R=R, SIR_threshold=10, inter_density=ll, sigma=8)['success_prob'])
#     print("6db, density {}, success prob {:.2f}".format(ll, psuccess_6dB[-1]))
#     print("10db, density {}, success prob {:.2f}".format(ll, psuccess_10dB[-1]))

# # plot
# sns.set_theme(style="white", font_scale=2, palette="Dark2")
# fig, ax = plt.subplots(figsize=(10,6))
# ms = 10
# lw = 2
# ls = '--'
# sns.lineplot(x=l, y=psuccess_6dB, ax=ax, label="threshold 6dB", lw=lw, marker="o", ms=ms, ls=ls)
# sns.lineplot(x=l, y=psuccess_10dB, ax=ax, label="threshold 10dB", lw=lw, marker="o", ms=ms, ls=ls)
# ax.set_xlabel(r"$\lambda$")
# ax.set_ylabel("success probability")
# ax.set_xscale("log")

# import os
# if not os.path.exists("figures"): os.makedirs("figures")
# fig.savefig("figures/GQRpacket_radio.pdf", bbox_inches='tight')


################################################################################
#                               Cellular system                                #
################################################################################
print("\n\nCELLULAR SYSTEM SIMULATION")
a = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
sns.set_theme(style="white", font_scale=2, palette="Dark2")

N = [1,3,4,7]
R0 = 0.91
Rs = [R0*np.sqrt(3*n) for n in N]
R1s = [r - R0 for r in Rs]
R2s = [r + R0 for r in Rs]

ms = 10
lw = 2
ls = '--'
for R,R1, R2,n in zip(Rs,R1s,R2s,N):
    outage_6dB = []
    outage_10dB = []
    for aa in a:
        np.random.seed(0)
        outage_6dB.append(GQR_cellular_system(R0, SIR_threshold=6, alpha=aa, sigma=8, eta=4, R1=R1, R2=R2)['failure_prob'])
        outage_10dB.append(GQR_cellular_system(R0, SIR_threshold=10, alpha=aa, sigma=8, eta=4, R1=R1, R2=R2)['failure_prob'])
        print("6db, prob alpha {}, outage prob {:.2f}".format(aa, outage_6dB[-1]))
        print("10db, prob alpha {}, outage prob {:.2f}".format(aa, outage_6dB[-1]))

    fig, ax = plt.subplots(figsize=(10,6))
    sns.lineplot(x=a, y=outage_6dB, ax=ax, label="threshold 6dB", lw=lw, marker="o", ms=ms, ls=ls)
    sns.lineplot(x=a, y=outage_10dB, ax=ax, label="threshold 10dB", lw=lw, marker="o", ms=ms, ls=ls)

    ax.set_xlabel(r"$\alpha$")
    ax.set_ylabel("outage probability")
    fig.savefig("figures/GQRcellular_system_N{}.pdf".format(n), bbox_inches='tight')

################################################################################
#                               Multi-access                                   #
################################################################################
# print("\n\nMULTI-ACCESS SIMULATION")
# G = [2+i*5 for i in range(0,20)]
# throughput_6dB = []
# throughput_10dB = []
# capture_probs_6dB = []
# capture_probs_10dB = []
# R = 1
# for gg in G:
#     np.random.seed(0)
#     r = GQRmulti_access(R, SIR_threshold=6, G=gg, sigma=8)
#     s = GQRmulti_access(R, SIR_threshold=10, G=gg, sigma=8)
#     throughput_6dB.append(r['success_prob'])
#     throughput_10dB.append(s['success_prob'])
#     capture_probs_6dB.append(r['capture_prob'])
#     capture_probs_10dB.append(s['capture_prob'])
#     print("6db, G {}, throughput {:.2f}".format(gg, throughput_6dB[-1]))
#     print("10db, G {}, throughput {:.2f}".format(gg, throughput_6dB[-1]))
#     print("6db, G {}, capture prob {}".format(gg, capture_probs_6dB[-1]))
#     print("10db, G {}, capture prob {}".format(gg, capture_probs_10dB[-1]))


# capture_probs_6dB = np.array(capture_probs_6dB)
# capture_probs_10dB = np.array(capture_probs_10dB)
# np.savetxt("capture_probs_6dB.txt", capture_probs_6dB)
# np.savetxt("capture_probs_10dB.txt", capture_probs_10dB)
# fig, ax = plt.subplots(figsize=(10,6))
# sns.lineplot(x=G, y=throughput_6dB, ax=ax, label="threshold 6dB", lw=lw, marker="o", ms=ms, ls=ls)
# sns.lineplot(x=G, y=throughput_10dB, ax=ax, label="threshold 10dB", lw=lw, marker="o", ms=ms, ls=ls)

# ax.set_xlabel("Average number of transmissions per slot")
# ax.set_ylabel("throughput")
# fig.savefig("figures/GQRmulti_access.pdf", bbox_inches='tight')

