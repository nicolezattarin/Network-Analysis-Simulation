from genericpath import exists
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from multihop import*

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--distance', type=int, default=5)
parser.add_argument('--N', type=int, default=100)
parser.add_argument('--density', type=int, default=10)

def main(distance, N, density):
    start = point(distance,0)
    destination = point(0,0)
    # np.random.seed()

    activation_prob = [0.03+0.01*i for i in range(1,101) if 0.03+0.01*i<1]
    average_active_nodes = np.pi * density * np.array(activation_prob)

    average_hops = []
    std_hops = []
    for a in activation_prob:
        print('activation prob:', a)
        hops = [avg_hops(density, a, destination, start) for i in range(N)]
        average_hops.append(np.mean(hops))
        std_hops.append(np.std(hops))

    # GAF
    from GAF import best_case, worst_case
    best_case_hops = best_case(distance) 
    worst_case_hops = worst_case(distance)

    #plot 
    import os
    if not os.path.exists('figures'): os.makedirs('figures')
    if not os.path.exists('results'): os.makedirs('results')
    np.savetxt('results/avg_hops_N{}_distance{}.txt'.format(N, distance), average_hops)
    np.savetxt('results/std_hops_N{}_distance{}.txt'.format(N, distance), std_hops)

    sns.set_theme(style="white", font_scale=2, palette = "inferno")
    fig, ax = plt.subplots(figsize=(8,6))
    ax.errorbar(average_active_nodes, average_hops, yerr=std_hops, color='teal', label='GeRaF', lw=2, linestyle='-')
    ax.scatter (15, best_case_hops, color='DarkOrange', label='GAF best case', marker='o', s=100)
    ax.scatter (15, worst_case_hops, color='DarkMagenta', label='GAF worst case', marker='o', s=100)
    ax.legend(loc='best')

    ax.set_xlabel('Average number of active nodes')
    ax.set_ylabel('Average number of hops')
    if distance == 5:
        ax.set_ylim(0, 40)
    elif distance == 10:
        ax.set_ylim(0, 80)
    elif distance == 20:
        ax.set_ylim(0, 160)



    fig.savefig('figures/multihop_GeRaF_N{}_distance{}.pdf'.format(N, distance), bbox_inches='tight')

if __name__ == '__main__':
    args = parser.parse_args()
    main(**vars(args))