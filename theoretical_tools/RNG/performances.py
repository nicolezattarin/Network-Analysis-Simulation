from RNG import random
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--sim", default='poisson', help="poisson or binomial.", type=str)


def main (sim):

    # time grid 
    n = [10**i for i in range(1,6)]
    p = [0.1*i for i in range(1,10)]    
    # each row corrrespond to a different n, each column to a different p
    grid_size = (len(n), len(p))
    N=100 # number of experiments over which computing the average
    
    # BINOMIAL
    if sim == 'binomial':
        grid_time_binomial_cdf = np.zeros(grid_size)
        grid_time_binomial_uniform = np.zeros(grid_size)
        grid_time_binomial_geometric = np.zeros(grid_size)

        # take the average time over N runs
        for nn in n:
            for pp in p:
                rand = random(seed=0)

                print ('n=', nn, 'p=', pp)
                grid_time_binomial_cdf[n.index(nn), p.index(pp)] = np.average(rand.binomial(n=nn, p=pp, size=N, 
                                                                        method='cdf', compute_time=True)[1])
                grid_time_binomial_uniform[n.index(nn), p.index(pp)] = np.average(rand.binomial(n=nn, p=pp, size=N, 
                                                                        method='uniform', compute_time=True)[1])
                grid_time_binomial_geometric[n.index(nn), p.index(pp)] = np.average(rand.binomial(n=nn, p=pp, size=N, 
                                                                        method='geometric', compute_time=True)[1])
        #save the results
        import os 
        if not os.path.exists('results'):
            os.makedirs('results')
        
        np.savetxt('results/binomial_cdf_time.txt', grid_time_binomial_cdf)
        np.savetxt('results/binomial_uniform_time.txt', grid_time_binomial_uniform)
        np.savetxt('results/binomial_geometric_time.txt', grid_time_binomial_geometric)

    # POISSON
    lam = [i for i in  range(1,25)]
    nlambdas = len(lam)
    N=1000

    if sim == 'poisson':
        grid_time_poisson_exp = np.zeros(nlambdas)
        grid_time_poisson_exp_opt = np.zeros(nlambdas)
        grid_time_poisson_cdf = np.zeros(nlambdas)
        # take the average time over N runs
        for l in lam:
                rand = random(seed=0)
                print ('lam =', l)
                grid_time_poisson_exp[lam.index(l)] = np.average(rand.poisson(lam=l, size=N, 
                                                                        method='exp', compute_time=True)[1])
                grid_time_poisson_exp_opt[lam.index(l)] = np.average(rand.poisson(lam=l, size=N, 
                                                                        method='exp_opt', compute_time=True)[1])
                grid_time_poisson_cdf[lam.index(l)] = np.average(rand.poisson(lam=l, size=N, 
                                                                        method='cdf', compute_time=True)[1])
        # save the results
        np.savetxt('results/poisson_exp_time.txt', grid_time_poisson_exp)
        np.savetxt('results/poisson_exp_opt_time.txt', grid_time_poisson_exp_opt)
        np.savetxt('results/poisson_cdf_time.txt', grid_time_poisson_cdf)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args.sim)