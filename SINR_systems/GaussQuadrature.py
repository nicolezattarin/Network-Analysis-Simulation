import numpy as np
from scipy import integrate

def GaussWeights(N):
    vs = np.loadtxt('GaussAbscissa/abs_{}.txt'.format(N), delimiter=',', dtype=float)
    ws = np.loadtxt('GaussWeights/ws_{}.txt'.format(N), delimiter=',', dtype=float)
    return ws, vs

def Quad(f, a, b, args, N=50):
    if N<4 or N>64: raise ValueError('N must be between 4 and 64')
    w, xs = GaussWeights(N)
    w = np.array(w)
    xs = np.array(xs)
    xs = ((b-a)*xs + a+b)/2
    w = (b-a)/2*w
    int = 0
    for ww, xx in zip(w, xs):
        int+=f(xx, *args)*ww
    return int

def GaussQuad(f, sigma, args, N=50):
    if N<4 or N>64: raise ValueError('N must be between 4 and 64')
    w, xs = GaussWeights(N)
    w = np.array(w)
    xs = np.array(xs)
    w = w/np.sqrt(np.pi)
    xs = xs*sigma*np.sqrt(2)
    int = 0
    for ww, xx in zip(w, xs):
        int+=f(xx, *args)*ww
    return int

def gauss(r, sigma):
    return 1/(sigma*np.sqrt(2*np.pi))*np.exp(-r**2/(2*sigma**2))

def GQR_packet_radio (r0, R, SIR_threshold, inter_density, sigma, eta=4):
    SIR_threshold = 0.1*np.log(10)*SIR_threshold
    sigma = 0.1*np.log(10)*sigma

    def Integral_r(xi, r0, xi_0, SIR_threshold, sigma, R, eta): 
        def func_r (r, xi, r0, xi_0, SIR_threshold, sigma, R, eta):#only r is var, all the rest is arg
            f = gauss(xi, sigma)*(2*r/R**2)*(1-1/(1+SIR_threshold*np.exp(xi_0-xi)*(r/r0)**-eta))
            return f
        args = (xi, r0, xi_0, SIR_threshold, sigma, R, eta)
        int = Quad(func_r, 0, R, args)
        return int
    
    def Integral_xi(r0, xi_0, SIR_threshold, sigma, R, eta): 
        def func_xi(xi, r0, xi_0, SIR_threshold, sigma, R, eta):
            f = Integral_r(xi, r0, xi_0, SIR_threshold, sigma, R, eta)
            return f
        args = (r0, xi_0, SIR_threshold, sigma, R, eta)
        int = GaussQuad(func_xi, sigma, args)
        return int
    
    def Integral_xi0(r0, SIR_threshold, inter_density, sigma, R, eta): 
        def func_xi0(xi_0, r0, SIR_threshold, inter_density, sigma, R, eta):
            f = np.exp(-inter_density*np.pi*R**2*(1-Integral_xi(r0, xi_0, SIR_threshold, sigma, R, eta)))
            return f
        args = (r0, SIR_threshold, inter_density, sigma, R, eta)
        int = GaussQuad(func_xi0, sigma, args)
        return int
    
    Ps = Integral_xi0(r0, SIR_threshold, inter_density, sigma, R, eta)
    r = {'success_prob': Ps, 'failure_prob': 1-Ps}
    return r

def GQR_cellular_system (r0, R, SIR_threshold, alpha, sigma, eta, R1, R2):
    # SIR_threshold = 0.1*np.log(10)*SIR_threshold
    # sigma = 0.1*np.log(10)*sigma
    SIR_threshold = 10**(SIR_threshold*0.1)
    sigma = 10**(sigma*0.1)

    def Integral_r(xi, r0, xi_0, SIR_threshold, sigma, R, eta, R1, R2):
        def func_r (r, xi, r0, xi_0, SIR_threshold, sigma, R, eta):#only r is var, all the rest is arg
            f = gauss(xi, sigma)*(2*r/R**2)*(1-1/(1+SIR_threshold*np.exp(xi_0-xi)*(r/r0)**-eta))
            return f
        args = (xi, r0, xi_0, SIR_threshold, sigma, R, eta)
        int = Quad(func_r, R1, R2, args)
        return int
    
    def Integral_xi(r0, xi_0, SIR_threshold, sigma, R, eta, R1, R2): 
        def func_xi(xi, r0, xi_0, SIR_threshold, sigma, R, eta, R1, R2):
            f = Integral_r(xi, r0, xi_0, SIR_threshold, sigma, R, eta, R1, R2)
            return f
        args = (r0, xi_0, SIR_threshold, sigma, R, eta, R1, R2)
        int = GaussQuad(func_xi, sigma, args)
        return int
    
    def Integral_xi0(r0, SIR_threshold, alpha, sigma, R, eta, R1, R2): 
        def func_xi0(xi_0, r0, SIR_threshold, alpha, sigma, R, eta, R1, R2):
            f = (1-alpha+alpha*Integral_xi(r0, xi_0, SIR_threshold, sigma, R, eta, R1, R2))**6
            return f
        args = (r0, SIR_threshold, alpha, sigma, R, eta, R1, R2)
        int = GaussQuad(func_xi0, sigma, args)
        return int
    
    def Integral_r0(SIR_threshold, alpha, sigma, R, eta, R1, R2): 
        def func_r0(r0, SIR_threshold, alpha, sigma, R, eta, R1, R2):
            f = (2*r0/R**2)*Integral_xi0(r0, SIR_threshold, alpha, sigma, R, eta, R1, R2)
            return f
        args = (SIR_threshold, alpha, sigma, R, eta, R1, R2)
        int = Quad(func_r0, 0, R, args)
        return int
    
    Ps = Integral_r0(SIR_threshold, alpha, sigma, R, eta, R1, R2)
    r = {'success_prob': Ps, 'failure_prob': 1-Ps}
    return r

def GQRmulti_access (r0, R, SIR_threshold, G, sigma, eta=4):
    SIR_threshold = 0.1*np.log(10)*SIR_threshold
    sigma = 0.1*np.log(10)*sigma

    def Integral_r(xi, r0, xi_0, SIR_threshold, sigma, R, eta): 
        def func_r (r, xi, r0, xi_0, SIR_threshold, sigma, R, eta):#only r is var, all the rest is arg
            f = gauss(xi, sigma)*(2*r/R**2)*(1-1/(1+SIR_threshold*np.exp(xi_0-xi)*(r/r0)**-eta))
            return f
        args = (xi, r0, xi_0, SIR_threshold, sigma, R, eta)
        int = Quad(func_r, 0, R, args)
        return int
    
    def Integral_xi(r0, xi_0, SIR_threshold, sigma, R, eta): 
        def func_xi(xi, r0, xi_0, SIR_threshold, sigma, R, eta):
            f = Integral_r(xi, r0, xi_0, SIR_threshold, sigma, R, eta)
            return f
        args = (r0, xi_0, SIR_threshold, sigma, R, eta)
        int = GaussQuad(func_xi, sigma, args)
        return int
    
    def Integral_xi0(r0, SIR_threshold, G, sigma, R, eta): 
        def func_xi0(xi_0, r0, SIR_threshold, G, sigma, R, eta):
            f = G*np.exp(-G*(1-Integral_xi(r0, xi_0, SIR_threshold, sigma, R, eta)))
            return f
        args = (r0, SIR_threshold, G, sigma, R, eta)
        int = GaussQuad(func_xi0, sigma, args)
        return int

    def Integral_r0(SIR_threshold, G, sigma, R, eta): 
        def func_r0(r0, SIR_threshold, G, sigma, R, eta):
            f = (2*r0/R**2)*Integral_xi0(r0, SIR_threshold, G, sigma, R, eta)
            return f
        args = (SIR_threshold, G, sigma, R, eta)
        int = Quad(func_r0, 0, 1, args)
        return int
    
    Ps = Integral_r0(SIR_threshold, G, sigma, R, eta)
    r = {'success_prob': Ps, 'failure_prob': 1-Ps}
    return r
