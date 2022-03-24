from RNG import random
import numpy as np

def main ():
    rand = random(seed=0)

    # time grid 
    n = [10**i for i in range(1,7)]
    p = [0.1*i for i in range(1,10)]

    # each row corrrespond to a different n, each column to a different p
    grid_size = (len(n), len(p))
    N=100 # number of experiments over which computing the average

    grid_time_binomial_cdf = np.zeros(grid_size)
    grid_time_binomial_uniform = np.zeros(grid_size)
    grid_time_binomial_geometric = np.zeros(grid_size)

    # take the average time over N runs
    for nn in n:
        for pp in p:
            print ('n=', nn, 'p=', pp)
            grid_time_binomial_cdf[n.index(nn), p.index(pp)] = np.average(rand.binomial(n=nn, p=pp, size=N, 
                                                                    method='cdf', compute_time=True)[1])
            grid_time_binomial_uniform[n.index(nn), p.index(pp)] = np.average(rand.binomial(n=nn, p=pp, size=N, 
                                                                    method='uniform', compute_time=True)[1])
            grid_time_binomial_geometric[n.index(nn), p.index(pp)] = np.average(rand.binomial(n=nn, p=pp, size=N, 
                                                                    method='geometric', compute_time=True)[1])
            print('puzzola')
    #save the results
    import os 
    if not os.path.exists('results'):
        os.makedirs('results')
    
    np.savetxt('results/binomial_cdf_time.txt', grid_time_binomial_cdf)
    np.savetxt('results/binomial_uniform_time.txt', grid_time_binomial_uniform)
    np.savetxt('results/binomial_geometric_time.txt', grid_time_binomial_geometric)

if __name__ == '__main__':
    main()