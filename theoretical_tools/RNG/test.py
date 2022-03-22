from RNG import random
import numpy as np

rand = random(seed=0)

print ("uniform", rand.uniform(0,1,size= 10))
print ("binomial uniform", rand.binomial (n=100, p=0.2, size=10, method='uniform'))
print ("binomial geometric", rand.binomial (n=100, p=0.2, size=10, method='geometric'))
