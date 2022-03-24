from distutils.log import warn
from timeit import timeit
import numpy as np
import time 

class random ():
    """
    Class that implements different random number genrators for simulation
    """
    def __init__(self, seed=None):
        """
        Constructor of the random class
        args:
            seed: seed for the random number generator
        """
        if seed is not None: self.seed = seed
        else: self.seed = 0
        
    def uniform (self, inf=0, sup=1, size=None, a=1103515245, b=12345, m=2**32):
        """
        Generate a random number between inf and sup
        args:
            inf: lower bound
            sup: upper bound
            size: number of random numbers to generate
            a: multiplier
            b: increment
            m: modulus
        """
        if size != None and size < 0:
            raise ValueError('size must be positive')
        if inf > sup:
            raise ValueError('inf must be lower than sup')
              
        def uniform (inf, sup, a, b, m):
            rand = (a*self.seed+b)%m
            self.seed = rand
            return rand

        if size == None or size == 1:
            rand = inf + (sup-inf)*uniform(inf,sup,a,b,m)/m 
        else :
            size = int(size)
            rand = np.zeros(size)
            for i in range(size):
                rand[i] = inf + (sup-inf)*uniform(0,1,a,b,m)/m
        return rand

    def geometric (self, p, size=None):
        """
        Geometric distribution
        args:
            p: probability of success
            size: number of random numbers to generate
        """
        if p < 0 or p > 1:
            raise ValueError('p must be between 0 and 1')
        
        def geometric (p):
            return np.floor(np.log(self.uniform(0,1))/np.log(1-p))
        
        if size == None or size == 1:
            rand = geometric(p)
        else :
            size = int(size)
            rand = np.zeros(size)
            for i in range(size):
                rand[i] = geometric(p)
        return rand

    def binomial (self, n, p, size=None, method='uniform', compute_time=False):
        # DEBUG: IMPLEMENT WITH P>0.5
        """
        Binomial distribution
        args:
            n: number of trials
            p: probability of success
            size: number of random numbers to generate
            method: 'cdf'
                    'geometric'
                    'uniform'
        """   
        if p < 0 or p > 1:
            raise ValueError('p must be between 0 and 1')
        if n < 0:
            raise ValueError('n must be positive')
        if size != None and size < 0:
            raise ValueError('size must be positive')

        m = method.lower()
        if m != 'cdf' and m != 'geometric' and m != 'uniform':
            raise ValueError('method must be one of cdf, geometric, poisson')
        
        def binomial_uniform (n,p, compute_time=False):

            if compute_time: t0 = time.time()
            test = self.uniform(0,1, size=n)
            prob = np.ones(n)*p
            success = prob-test>=0
            if compute_time: t = time.time()-t0
            else: t = None
            return np.sum(success), t
        
        def binomial_geometric (n,p, compute_time=False):
            if compute_time: t0 = time.time()
            n_trials = 0
            rand = 0
            while n_trials<=n:
                rand += 1
                trial = self.geometric(p)
                n_trials += trial + 1 # all the failures + success
            if compute_time: t = time.time()-t0
            else: t = None
            return rand, t

        def binomial_cdf (n,p, compute_time=False):
            """
            based on the trick for binomial distribution: p_{k+1} = p_k * (n-k)/(k+1) * p/(1-p)
            """

            if compute_time: t0 = time.time()
            coef = p/(1-p) # coefficient 
            u = self.uniform(0,1) # extract a value of CDF
            if p<=0.5:
                pr = (1-p)**n # probability of zero successes
                F = pr # CDF for zero successes
                rand = 0 # start from k=0
                while u>=F:
                    pr *= coef*(n-rand)/(rand+1)
                    F += pr
                    rand += 1
                    if pr < 1e-10: break
                if compute_time: t = time.time()-t0
                else: t = None
                return rand, t
            else:
                u = self.uniform(0,1)
                pr = p**n # probability of zero failures
                F = 1 # CDF for zero failures
                rand = n # start from k=n
                while u<=F:
                    # print('iter ', u, F, pr, rand)
                    pr *= rand/(n-rand+1)/coef
                    F -= pr
                    rand -= 1
                    if rand == 0: break
                    if pr < 1e-10: break
                if compute_time: t = time.time()-t0
                else: t = None
                return rand, t

        if size == None or size == 1:
            rand = 0
            size = 1
        else :
            size = int(size)
            rand = np.zeros(size)
            t = np.zeros(size)
        
        if m == 'uniform':
            if size != 1:
                for i in range(size):
                    rand[i], t[i] = binomial_uniform(n,p,compute_time)
            else: rand, t = binomial_uniform(n,p,compute_time)
        elif m == 'geometric':
            if size != 1:
                for i in range(size):
                    rand[i], t[i] = binomial_geometric(n,p,compute_time)
            else: rand,t = binomial_geometric(n,p,compute_time)
        elif m == 'cdf':
            if size != 1:
                for i in range(size):
                    rand[i], t[i] = binomial_cdf(n,p,compute_time)
            else: rand, t  = binomial_cdf(n,p,compute_time)
        return rand,t

    def exp(self, lam=1, size=None):
        """
        Exponential distribution
        args:
            lam: lambda
            size: number of random numbers to generate
        """
        if size == None or size == 1:
            rand = -self.uniform(0,1)/lam
        else :
            size = int(size)
            rand = np.zeros(size)
            for i in range(size):
                rand[i] = -np.log(self.uniform(0,1))/lam
        return rand

    def poisson (self, lam=0, size=None, method='exp'):
        """
        Poisson distribution
        args:
            lambda: parameter
            size: number of random numbers to generate
            method: 'cdf'
                    'exp'
                    'exp_opt'
        """
        m = method.lower()
        if m != 'cdf' and m != 'exp' and m != 'exp_opt':
            raise ValueError('method must be one of cdf, log, exp')
        
        def poisson_exp (lam):
            t = -np.log(self.uniform(0,1))/lam
            rand = 1
            while t <= 1:
                t += -np.log(self.uniform(0,1))/lam
                rand += 1
            return rand-1

        def poisson_exp_opt (lam):
            sup = np.exp(-lam)
            rand = 1
            prod = self.uniform(0,1)

            while prod >= sup:
                prod *= self.uniform(0,1)
                rand += 1
            return rand-1
        
        def poisson_cdf(lam):
            u = self.uniform(0,1)
            rand = 0
            p = np.exp(-lam)
            F = p
            while u>=F:
                p *= lam/(rand+1)
                F += p
                rand+=1
            return rand
 
        if m == 'exp':
            if size == None or size == 1:
                rand = poisson_exp(lam)
            else :
                size = int(size)
                rand = np.zeros(size)
                for i in range(size):
                    rand[i] = poisson_exp(lam)
        elif m == 'exp_opt':
            if size == None or size == 1:
                rand = poisson_exp_opt(lam)
            else :
                size = int(size)
                rand = np.zeros(size)
                for i in range(size):
                    rand[i] = poisson_exp_opt(lam)
        elif m == 'cdf':
            if size == None or size == 1:
                rand = poisson_cdf(lam)
            else :
                size = int(size)
                rand = np.zeros(size)
                for i in range(size):
                    rand[i] = poisson_cdf(lam)
        return rand


