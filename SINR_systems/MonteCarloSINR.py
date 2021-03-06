#SINR performance 
import numpy as np

def BoxMuller (mu, sigma):
    """
    params:
    mu: mean
    sigma: variance
    """
    u1 = np.random.uniform()
    u2 = np.random.uniform()
    z1 = np.sqrt(-2*np.log(u1))*np.cos(2*np.pi*u2)
    z2 = np.sqrt(-2*np.log(u1))*np.sin(2*np.pi*u2)
    return mu + z1*sigma

def packet_radio(r0, R, SIR_threshold, inter_density, sigma, eta=4, maxiter=10000, verbose=True):
    """
    params:
    r0: position of object
    R: maximal distance
    SIR_threshold: SIR threshold
    inter_density: density of interfering objects
    sigma: variance of the gaussian distribution
    eta: exponent of the distance
    maxiter: number of iterations
    verbose: print progress

    """
    np.random.seed(0)
    #assuming that threshold and sigma are given in dB, we need to convert to base e
    SIR_threshold = 0.1*np.log(10)*SIR_threshold
    sigma = 0.1*np.log(10)*sigma
    successes = 0
    for t in range(maxiter):
        # k, number of interferes, is poisson with param lambda pi R^2
        k = np.random.poisson(lam=np.pi*inter_density*R**2)
        # for all k points we generate xi gaussian wirth mean 0 and variance sigma, Ri exponential with unit mean
        # ri is the distance from the transmitter to the interferer, thus uniform in [0, R]
        xi = np.array([BoxMuller (0, sigma) for i in range(k)])
        RR = np.array([np.random.exponential(1/2) for i in range(k)])
        r = np.array([R*np.random.uniform()**0.5 for i in range(k)])
        xi_0 = np.random.normal(0, sigma)
        RR_0 = np.random.exponential(1/2)
        checkvar = RR_0*np.exp(xi_0)*r0**(-eta)/(np.sum(RR*np.exp(xi)*r**(-eta)))
        if checkvar > SIR_threshold: successes += 1
        if verbose and t%100==0: 
            print(" iter {:.2f}, k {:.2f}, checkvar {:.2f}, threshold {:.2f}, successes {:.2f}"\
                .format(t, k, checkvar, SIR_threshold, successes))

    if verbose: 
        print("successes prob: {:.2f}".format(successes/maxiter))
        print("successes: {:.2f}".format(successes))
        print("failures: {:.2f}".format(maxiter-successes))
    r = {'successes': successes, 'failures': maxiter-successes, 
        'success_prob': successes/maxiter, 'failure_prob': (maxiter-successes)/maxiter}
    return r

def cellular_system(R, N, SIR_threshold, alpha, sigma, eta=4, maxiter=10000, verbose=True):
    """
    params:
    R: maximal distance
    N: reuse factor
    SIR_threshold: SIR threshold
    alpha: interfering probability
    sigma: variance of the gaussian distribution
    eta: exponent of the distance
    maxiter: number of iterations
    verbose: print progress
    """
    np.random.seed(0)
    
    # we average als over 
    #assuming that threshold and sigma are given in dB, we need to convert to base e
    SIR_threshold = 0.1*np.log(10)*SIR_threshold
    sigma = 0.1*np.log(10)*sigma
    successes = 0
    for t in range(maxiter):
        # k, number of interferes
        k = np.random.binomial(6, alpha)
        if k == 0:
            successes += 1
            continue
        # for all k points we generate xi gaussian wirth mean 0 and variance sigma, Ri exponential with unit mean
        # ri is the distance from the transmitter to the interferer, thus uniform in [0, R]
        xi = np.array([BoxMuller (0, sigma) for i in range(k)])
        RR = np.array([np.random.exponential(1/2) for i in range(k)])
        # (sqrt(3*N)*R)-R)+ (2*R*rand())
        # r = np.array([R+R*np.random.uniform()**0.5 for i in range(k)])
        r = np.array([np.sqrt(3*N)*R-R +2*R*np.random.uniform() for i in range(k)])
        xi_0 = np.random.normal(0, sigma)
        RR_0 = np.random.exponential(1/2)
        r0 = R*np.sqrt(np.random.uniform())
        checkvar = RR_0*np.exp(xi_0)*r0**(-eta)/(np.sum(RR*np.exp(xi)*r**(-eta)))
        if checkvar > SIR_threshold: successes += 1
        if verbose and t%100==0: 
            print(" iter {:.2f}, k {:.2f}, checkvar {:.2f}, threshold {:.2f}, successes {:.2f}"\
                .format(t, k, checkvar, SIR_threshold, successes))

    if verbose: 
        print("successes prob: {:.2f}".format(successes/maxiter))
        print("successes: {:.2f}".format(successes))
        print("failures: {:.2f}".format(maxiter-successes))

    r = {'successes': successes, 'failures': maxiter-successes, 
        'success_prob': successes/maxiter, 'failure_prob': (maxiter-successes)/maxiter}
    return r

def multi_access(R, SIR_threshold, G, sigma, eta=4, maxiter=10000, verbose=True):
    """
    params:
    r0: position of object
    R: maximal distance
    SIR_threshold: SIR threshold
    G: average number of transmissions per slot
    sigma: variance of the gaussian distribution
    eta: exponent of the distance
    maxiter: number of iterations
    verbose: print progress
    """
    np.random.seed(0)
    #assuming that threshold and sigma are given in dB, we need to convert to base e
    SIR_threshold = 0.1*np.log(10)*SIR_threshold
    sigma = 0.1*np.log(10)*sigma
    successes = 0
    for t in range(maxiter):
        k = np.random.poisson(G) #number of users
        if k == 0: 
            # no users in the system
            print("no users")
            continue
        # for all k points we generate xi gaussian wirth mean 0 and variance sigma, Ri exponential with unit mean
        # ri is the distance from the transmitter to the interferer, thus uniform in [0, R]
        xi = np.array([BoxMuller (0, sigma) for i in range(k)])
        RR = np.array([ np.random.exponential(1/2) for i in range(k)])
        r = np.array([R*np.random.uniform()**0.5 for i in range(k)])
        checkvar = np.max(RR*np.exp(xi)*r**(-eta))/(np.sum(RR*np.exp(xi)*r**(-eta)))
        if checkvar > SIR_threshold/(1+SIR_threshold): successes += 1
        if verbose and t%100==0: 
            print(" iter {:.2f}, k {:.2f}, checkvar {:.2f}, threshold {:.2f}, successes {:.2f}"\
                .format(t, k, checkvar, SIR_threshold, successes))

    if verbose: 
        print("successes prob: {:.2f}".format(successes/maxiter))
        print("successes: {:.2f}".format(successes))
        print("failures: {:.2f}".format(maxiter-successes))

    r = {'successes': successes, 'failures': maxiter-successes, 
        'success_prob': successes/maxiter, 'failure_prob': (maxiter-successes)/maxiter}
    return r