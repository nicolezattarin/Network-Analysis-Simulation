from RNG import random
import numpy as np

rand = random(seed=1)

print ("uniform wide", rand.uniform(0,1,size=10, method='wide'))
print ("binomial cdf <0.5", rand.binomial (n=100, p=0.2, size=10, method='cdf')[0])
print ("binomial cdf >0.5", rand.binomial (n=100, p=0.8, size=10, method='cdf')[0])

print ("binomial uniform", rand.binomial (n=1000, p=0.2, size=10, method='uniform')[0])
print ("binomial geometric", rand.binomial (n=1000, p=0.2, size=10, method='geometric')[0])
print ("exponential", rand.exp(lam=1, size=10))
print ("poisson exp", rand.poisson(lam=10, size=10, method='exp'))
print ("poisson opt", rand.poisson(lam=10, size=10, method='exp_opt'))
print ("poisson cdf ", rand.poisson(lam=10, size=10, method='cdf'))

