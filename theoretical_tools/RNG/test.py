from RNG import random
import numpy as np

rand = random(seed=0)

print ("uniform", rand.uniform(0,1,size= 10))
print ("binomial cdf", rand.binomial (n=1000, p=0.2, size=10, method='cdf'))
print ("binomial uniform", rand.binomial (n=1000, p=0.2, size=10, method='uniform'))
print ("binomial geometric", rand.binomial (n=1000, p=0.2, size=10, method='geometric'))
print ("exponential", rand.exp(lam=1, size=10))
print ("poisson", rand.poisson(lam=10, size=10, method='exp'))
print ("poisson", rand.poisson(lam=10, size=10, method='exp_opt'))
print ("poisson", rand.poisson(lam=10, size=10, method='cdf'))

