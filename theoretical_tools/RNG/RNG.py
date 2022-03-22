import numpy as np

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
        
    def uniform (self, inf=0, sup=1,size=None, a=1103515245, b=12345, m=2**32):
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


    def binomial (self, n, p, size=None, method='uniform'):
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
        m = method.lower()
        if m != 'cdf' and m != 'geometric' and m != 'uniform':
            raise ValueError('method must be one of cdf, geometric, poisson')
        
        def binomial_uniform (n,p):
            """
            Binomial distribution
            args:
                n: number of trials
                p: probability of success
            """
            test = self.uniform(0,1, size=n)
            prob = np.ones(n)*p
            success = prob-test>=0
            return np.sum(success)
        
        def binomial_geometric (n,p):
            n_trials = 0
            rand = 0
            while n_trials<=n:
                rand += 1
                trial = np.random.geometric(p)
                n_trials += trial + 1 # all the failures + success
            return rand

        def binomial_cdf (n,p):
            u = self.uniform(0,1)
            c = p/(1-p) 
            pr = (1-p)**n
            F = pr
            rand = 0
            while u>=F:
                pr += c*(n-rand)/(rand+1)*pr
                F += pr
                rand += 1
            return rand -1
        
        if size == None or size == 1:
            rand = 0
            size = 1
        else :
            size = int(size)
            rand = np.zeros(size)
        
        if m == 'uniform':
            if size != 1:
                rand = [binomial_uniform(n,p) for i in range(size)]
            else: rand = binomial_uniform(n,p)
        elif m == 'geometric':
            if size != 1:
                rand = [binomial_geometric(n,p) for i in range(size)]
            else: rand = binomial_geometric(n,p)
        elif m == 'cdf':
            if size != 1:
                rand = [binomial_cdf(n,p) for i in range(size)]
            else: rand = binomial_cdf(n,p)

        return rand

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
            return rand -1
        
        def poisson_cdf(lam):
            u = self.uniform(0,1)
            p = np.exp(-lam)
            F = p
            rand = 0
            while u>=F:
                p *= lam/(rand+1)
                F += p
                rand+=1
            return rand-1
 
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


