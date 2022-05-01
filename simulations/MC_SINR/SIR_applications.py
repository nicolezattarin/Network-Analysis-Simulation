#SINR performance 
import numpy as np
def packet_radio(r0, R, SIR_threshold, inter_density, sigma, eta=4, maxiter=1000, verbose=True):
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
    #assuming that threshold and sigma are given in dB, we need to convert to base e
    SIR_threshold = 0.1*np.log(10)*SIR_threshold
    sigma = 0.1*np.log(10)*sigma
    successes = 0
    for t in range(maxiter):
        # k, number of interferes, is poisson with param lambda pi R^2
        k = np.random.poisson(lam=np.pi*inter_density*R**2)
        # for all k points we generate xi gaussian wirth mean 0 and variance sigma, Ri exponential with unit mean
        # ri is the distance from the transmitter to the interferer, thus uniform in [0, R]
        xi = np.array([np.random.normal(0, sigma) for i in range(k)])
        RR = np.array([np.random.exponential(1) for i in range(k)])
        r = np.array([R*np.random.uniform()**0.5 for i in range(k)])
        xi_0 = np.random.normal(0, sigma)
        R_0 = np.random.exponential(1)
        checkvar = R_0**2*np.exp(xi_0)*r0**(-eta)/(np.sum(RR**2*np.exp(xi)*r**(-eta)))
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

def cellular_system(r0, R, SIR_threshold, alpha, sigma, eta=4, maxiter=1000, verbose=True):
    """
    params:
    r0: position of object
    R: maximal distance
    SIR_threshold: SIR threshold
    alpha: interfering probability
    sigma: variance of the gaussian distribution
    eta: exponent of the distance
    maxiter: number of iterations
    verbose: print progress
    """
    #assuming that threshold and sigma are given in dB, we need to convert to base e
    SIR_threshold = 0.1*np.log(10)*SIR_threshold
    sigma = 0.1*np.log(10)*sigma
    successes = 0
    for t in range(maxiter):
        # k, number of interferes, is poisson with param lambda pi R^2
        k = np.random.binomial(6, alpha)
        # for all k points we generate xi gaussian wirth mean 0 and variance sigma, Ri exponential with unit mean
        # ri is the distance from the transmitter to the interferer, thus uniform in [0, R]
        xi = np.array([np.random.normal(0, sigma) for i in range(k)])
        RR = np.array([np.random.exponential(1) for i in range(k)])
        r = np.array([R*np.random.uniform()**0.5 for i in range(k)])
        xi_0 = np.random.normal(0, sigma)
        R_0 = np.random.exponential(1)
        checkvar = R_0**2*np.exp(xi_0)*r0**(-eta)/(np.sum(RR**2*np.exp(xi)*r**(-eta)))
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

def multi_access(r0, R, SIR_threshold, G, sigma, eta=4, maxiter=1000, verbose=True):
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
    #assuming that threshold and sigma are given in dB, we need to convert to base e
    SIR_threshold = 0.1*np.log(10)*SIR_threshold
    sigma = 0.1*np.log(10)*sigma
    successes = 0
    for t in range(maxiter):
        # k, number of interferes, is poisson with param lambda pi R^2
        k = np.random.poisson(G)
        if k == 0: 
            successes += 1 #if no interferers, we are successful by definition
            continue
        # for all k points we generate xi gaussian wirth mean 0 and variance sigma, Ri exponential with unit mean
        # ri is the distance from the transmitter to the interferer, thus uniform in [0, R]
        xi = np.array([np.random.normal(0, sigma) for i in range(k)])
        RR = np.array([np.random.exponential(1) for i in range(k)])
        r = np.array([R*np.random.uniform()**0.5 for i in range(k)])
        checkvar = np.max(RR**2*np.exp(xi)*r**(-eta))/(np.sum(RR**2*np.exp(xi)*r**(-eta)))
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