import numpy as np
from RNG import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    rand = random(seed=0)
    # Binomial distribution
    # We test the generation of a Binomial RV with three different methods (CDF inversion, 
    # using a sequence of n Bernoulli variables, using geometric strings of zeros),
    #  and then compare the time it takes to produce a large number of iid variates for 
    # different values of n and p
    #load matrices from file
    grid_time_binomial_cdf = pd.read_csv('results/binomial_cdf_time.txt', header=None, sep=' ')
    grid_time_binomial_uniform = pd.read_csv('results/binomial_uniform_time.txt', header=None, sep=' ')
    grid_time_binomial_geometric = pd.read_csv('results/binomial_geometric_time.txt', header=None, sep=' ')
    grid_time_binomial_cdf.columns = ['p_0.{}'.format(i) for i in range(1,len(grid_time_binomial_cdf.columns)+1)]
    grid_time_binomial_uniform.columns = ['p_0.{}'.format(i) for i in range(1,len(grid_time_binomial_uniform.columns)+1)]
    grid_time_binomial_geometric.columns = ['p_0.{}'.format(i) for i in range(1,len(grid_time_binomial_geometric.columns)+1)]

    n = [r'$10^{}$'.format(i) for i in range(1,len(grid_time_binomial_cdf.index)+1)]
    p = ['{:.1f}'.format(0.1*i) for i in range(1,len(grid_time_binomial_cdf.columns)+1)]

    fig,ax=plt.subplots(1,2, figsize=(16,6))
    sns.set_theme(style='white',palette='Dark2',font_scale=2)
    lw=2
    ms=10
    ls = '--'
    m = 'o'
    col = 0  
    for l in ['uniform','geometric']:
        a = pd.read_csv('results/binomial_%s_time.txt' % l, header=None, sep=' ')
        for i in range(len(grid_time_binomial_cdf.index)):
            g=sns.lineplot(x=p, y=a.iloc[i,:], ax=ax[col], linewidth=lw, markersize=ms, linestyle=ls,
                        marker=m, label='n={}'.format(n[i]))
            
        g.legend(loc='center left', bbox_to_anchor=(1, 0.5), borderaxespad=0.)
        col+=1
    ax[0].get_legend().remove()
    ax[0].set_yscale('log')
    ax[1].set_yscale('log')
    ax[0].set_ylim(0.7*10**-5, 1)
    ax[1].set_ylim(ax[0].get_ylim())
    ax[0].set_ylabel('time (s)')
    ax[1].set_ylabel('')
    ax[0].set_xlabel('probability')
    ax[1].set_xlabel('probability')
    ax[0].set_title('Uniform RV')
    ax[1].set_title('Geometric RV')
    ax[1].set_yticklabels([])
    fig.subplots_adjust(hspace=.0, wspace=0.03)
    fig.savefig('results/binomial_time_unif_cdf.pdf', bbox_inches='tight')

    fig,ax=plt.subplots(figsize=(10,6))
    sns.set_theme(style='white',palette='Dark2',font_scale=2)
    for i in range(len(grid_time_binomial_cdf.index)):
            g=sns.lineplot(x=p, y=grid_time_binomial_cdf.iloc[i,:], ax=ax, linewidth=lw, markersize=ms, linestyle=ls,
                        marker=m, label='n={}'.format(n[i]))
    g.legend(loc='center left', bbox_to_anchor=(1, 0.5), borderaxespad=0.)
    ax.set_ylabel('time (s)')
    ax.set_xlabel('probability')
    ax.set_yscale('log')

    # Poisson distribution
    # We test the generation of a Poisson RV with three different methods 
    # (CDF inversion, generating elements with exponential distribution and its optimized version),
    #  and then compare the time it takes to produce a large number of iid variates for 
    #  different values of $\lambda$

    grid_time_pois_cdf = np.loadtxt('results/poisson_cdf_time.txt')
    grid_time_pois_exp = np.loadtxt('results/poisson_exp_time.txt')
    grid_time_pois_exp_opt = np.loadtxt('results/poisson_exp_opt_time.txt')
    lam = [i for i in  range(1,25)]

    fig, ax = plt.subplots(figsize=(10,7))
    sns.set_theme(style='white',palette='Dark2',font_scale=2)
    sns.lineplot(x=lam, y=grid_time_pois_cdf, ax=ax, linewidth=lw, markersize=ms, linestyle=ls,
                        marker=m, label='CDF')
    g=sns.lineplot(x=lam, y=grid_time_pois_exp, ax=ax, linewidth=lw, markersize=ms, linestyle=ls,
                        marker=m, label='exp')
    g=sns.lineplot(x=lam, y=grid_time_pois_exp_opt, ax=ax, linewidth=lw, markersize=ms, linestyle=ls,
                        marker=m, label='exp optimized')
    ax.set_ylabel('time (s)')
    ax.set_xlabel(r'$\lambda$')
    ax.set_yscale('log')
    ax.set_ylim(0.8*10**-6, 0.7*10**-4)
    ax.set_yticks([10**-6, 10**-5, 10**-4])
    ax.legend(loc='lower right')
    fig.savefig('results/poisson_time.pdf', bbox_inches='tight')

if __name__ == '__main__':
    main()