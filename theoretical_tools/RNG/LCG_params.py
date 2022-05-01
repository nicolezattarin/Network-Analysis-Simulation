import numpy as np
from RNG import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from RNG import random
def main():
    # Consider the two LCGs: LCG1: a = 18, m = 101; LCG2: a = 2, m = 101
    rng1 = random(1)
    rng2 = random(1)
    N=301

    lcg1 = rng1.uniform(0,1,size=N, method='wide', a=18, m=101)
    lcg2 = rng2.uniform(0,1,size=N, method='wide', a=2, m=101)

    # Check whether they are full period: The period P is at most m, but can be smaller 
    # depending on the other parameters. If the period is m, the LCG is said to have full period.
    full_period_lcg1 = True
    full_period_lcg2 = True

    def check_full_period(a, m, seed):
        rng = random(seed)
        r = rng.uniform(0,1,size=m, method='wide', a=a, m=m)
        for i in range(1,m):
            if r[i] == r[0] and i!=m-1:
                return "period is {}, less than m".format(i)
            elif r[i] == r[0] and i==m-1:
                return "period is m ({}), the PRNG is full period".format(m)
        return "period is {}, more than m".format(i)

    print("LCG 1:", check_full_period(18, 101, 1))
    print("LCG 2:", check_full_period(2, 101, 1))

    # Plot all pairs (Ui, Ui+1) in a unit square and comment the results

    fig, ax = plt.subplots(1,2,figsize=(18,5))
    size = 30
    sns.set_theme(style='white',palette='Dark2',font_scale=2)
    sns.scatterplot(x=lcg1[1:], y=np.roll(lcg1, 1)[1:], color='teal',ax=ax[0],  marker='o', s=size)
    sns.scatterplot(x=lcg2[1:], y=np.roll(lcg2, 1)[1:], color='teal',ax=ax[1],  marker='o', s=size)
    ax[0].set_title('LCG1 (a=18, m=101)')
    ax[1].set_title('LCG2 (a=2, m=101)')
    ax[0].set_xlabel(r'$U_i$')
    ax[1].set_xlabel(r'$U_i$')
    ax[0].set_ylabel(r'$U_{i+1}$')
    ax[1].set_ylabel(r'$U_{i+1}$')
    fig.savefig('results/lcg_params_study.pdf', bbox_inches='tight')

    # 5. Consider the LCG with a = 65539, m = 2^31
    # a. Plot all pairs (Ui, Ui+1) in a unit square and comment the results
    rng = random(1)
    N=1000

    lcg = rng1.uniform(0,1,size=N, method='wide', a=65539, m=2**(31))

    fig, ax = plt.subplots(figsize=(10,6))
    size = 30
    sns.set_theme(style='white',palette='Dark2',font_scale=2)
    sns.scatterplot(x=lcg[1:], y=np.roll(lcg, 1)[1:], color='teal',ax=ax,  marker='o', s=size)
    ax.set_title(r'LCG (a = 65539, m = $2^{31}$)')
    ax.set_xlabel(r'$U_i$')
    ax.set_ylabel(r'$U_{i+1}$')
    fig.savefig('results/lcg_uniform.pdf', bbox_inches='tight')

    # b. Plot all triples (Ui, Ui+1, Ui+2) in a unit cube and comment the results
    size = 40
    x = lcg[2:]
    y = np.roll(lcg, 1)[2:]
    z = np.roll(lcg, 2)[2:]
    sns.set_theme(style='white',palette='Dark2',font_scale=1.2)

    fig = plt.figure(figsize=(18, 6))
    ax = fig.add_subplot(131, projection = '3d')
    ax.set_xlabel(r'$U_i$')
    ax.set_ylabel(r'$U_{i+1}$')
    ax.set_zlabel(r"$U_{i+2}$")
    ax.scatter(x, y, z, c='teal', marker='o', s=size)
    ax.view_init(20, 30)
    ax2 = fig.add_subplot(132, projection = '3d')
    ax2.set_xlabel(r'$U_i$')
    ax2.set_ylabel(r'$U_{i+1}$')
    ax2.set_zlabel(r"$U_{i+2}$")
    ax2.scatter(x, y, z, c='teal', marker='o', s=size)
    ax2.view_init(-210, -120)
    ax3 = fig.add_subplot(133, projection = '3d')
    ax3.set_xlabel(r'$U_i$')
    ax3.set_ylabel(r'$U_{i+1}$')
    ax3.set_zlabel(r"$U_{i+2}$")
    ax3.scatter(x, y, z, c='teal', marker='o', s=size)
    ax3.view_init(-210, -90)
    fig.savefig('results/lcg_3d.pdf', bbox_inches='tight')

if __name__ == "__main__":
    main()