import numpy as np
N_GQR = 20

def Quad(f, a, b, args=(), N=N_GQR):
    """
    integrate f with gauss quadrature
    """
    xs, w = np.polynomial.legendre.leggauss(N)
    #debug
    # print('LEGENDRE')
    # print('weights ', w)
    # print('x ', xs)
    # if len(xs) != len(w): print("lengths dont match")

    w = np.array(w)
    xs = np.array(xs)
    xs = ((b-a)*xs+a+b)/2
    w = (b-a)/2*w
    
    int = np.sum([f(xx, *args)*ww for xx, ww in zip(xs, w)])
    return int

def GaussQuad(f, sigma, args=(), N=N_GQR):
    """
    integrate f with gauss hermite quadrature
    """
    xs, w = np.polynomial.hermite.hermgauss(N)
    #debug
    # print('HERMITE')
    # print('weights ', w)
    # print('x ', xs)
    # if len(xs) != len(w): print("lengths dont match")

    w = np.array(w)
    xs = np.array(xs)
    w = w/np.sqrt(np.pi)
    xs = xs*sigma*np.sqrt(2)

    int = np.sum([f(xx, *args)*ww for xx, ww in zip(xs, w)])
    return int
 
def gauss(r, sigma):
    """
    Gaussian distribution
    """
    return 1/(sigma*np.sqrt(2*np.pi))*np.exp(-r**2/(2*sigma**2))

def GQR_packet_radio (r0, R, SIR_threshold, inter_density, sigma, eta=4):
    """
    Integration with Gaussian Quadrature rules for packet radio system
    """
    SIR_threshold = 0.1*np.log(10)*SIR_threshold
    sigma = 0.1*np.log(10)*sigma
    #DEBUG
    # print('threshold', SIR_threshold)

    def Integral_r(xi, r0, xi_0, SIR_threshold, R, eta): 
        def func_r (r, xi, xi_0, r0, SIR_threshold, R, eta):#only r is var, all the rest is arg
            f = (2*r/R**2)*(1-1/(1+SIR_threshold*np.exp(xi-xi_0)*(r/r0)**-eta))
            return f
        args = (xi, xi_0, r0, SIR_threshold, R, eta)
        int = Quad(func_r, 0, R, args)
        return int
    
    def Integral_xi(r0, xi_0, SIR_threshold, sigma, R, eta): 
        def func_xi(xi, r0, xi_0, SIR_threshold, R, eta):
            f = Integral_r(xi, r0, xi_0, SIR_threshold, R, eta)
            #DEBUG
            # print('f {:.3f}, threshold {}'.format(f, SIR_threshold))
            return f
        args = (r0, xi_0, SIR_threshold, R, eta)
        int = GaussQuad(func_xi, sigma, args)
        return int
    
    def Integral_xi0(r0, SIR_threshold, inter_density, sigma, R, eta): 
        def func_xi0(xi_0, r0, SIR_threshold, inter_density, sigma, R, eta):
            f = np.exp(-inter_density*np.pi*R**2*(Integral_xi(r0, xi_0, SIR_threshold, sigma, R, eta)))
            return f
        args = (r0, SIR_threshold, inter_density, sigma, R, eta)
        int = GaussQuad(func_xi0, sigma, args)
        return int
    
    Ps = Integral_xi0(r0, SIR_threshold, inter_density, sigma, R, eta)
    r = {'success_prob': Ps, 'failure_prob': 1-Ps}
    return r

def GQR_cellular_system (R, SIR_threshold, alpha, sigma, eta, R1, R2):
    """
    Integration with Gaussian Quadrature rules for cellular system
    params:
    R: range of the system
    SIR_threshold: SIR threshold
    alpha: probability of interference
    sigma: standard deviation of the Gaussian distribution
    eta: parameter of the power law
    R1: position of lower angle of the interfering cell
    R2: position of upper angle of the interfering cell
    """
    SIR_threshold = 0.1*np.log(10)*SIR_threshold
    sigma = 0.1*np.log(10)*sigma

    def Integral_r(xi, r0, xi_0, SIR_threshold, sigma, R, eta, R1, R2):
        def func_r (r, xi, r0, xi_0, SIR_threshold, sigma, R, eta):#only r is var, all the rest is arg
            f = (2*r/(R2**2-R1**2))*(1-1/(1+SIR_threshold*np.exp(xi-xi_0)*(r/r0)**-eta))
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
            f = (1-alpha*Integral_xi(r0, xi_0, SIR_threshold, sigma, R, eta, R1, R2))**6
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

def GQRmulti_access (R, SIR_threshold, G, sigma, eta=4, collision_size=np.arange(1,11,1)):
    """
    Gaussian Quadrature rules for multi-access system
    params:
    R: range of the system
    SIR_threshold: SIR threshold
    G: average number of transmissions per slot
    sigma: standard deviation of the Gaussian distribution
    eta: parameter of the power law
    collision_size: sizes to compute collision proability    
    """
    SIR_threshold = 0.1*np.log(10)*SIR_threshold
    sigma = 0.1*np.log(10)*sigma

    def Integral_r(xi, r0, xi_0, SIR_threshold, R, eta): 
        def func_r (r, xi, r0, xi_0, SIR_threshold, R, eta):#only r is var, all the rest is arg
            f = (2*r/R**2)*(1-1/(1+SIR_threshold*np.exp(xi-xi_0)*(r/r0)**-eta))
            return f
        args = (xi, r0, xi_0, SIR_threshold, R, eta)
        int = Quad(func_r, 0, 1, args)
        return int
    
    def Integral_xi(r0, xi_0, SIR_threshold, sigma, R, eta): 
        def func_xi(xi, r0, xi_0, SIR_threshold, R, eta):
            f = Integral_r(xi, r0, xi_0, SIR_threshold, R, eta)
            #DEBUG
            # print('f {:.3f}, threshold {}'.format(f, SIR_threshold))
            return f
        args = (r0, xi_0, SIR_threshold, R, eta)
        int = GaussQuad(func_xi, sigma, args)
        return int

    def Integral_r0(xi_0, SIR_threshold, G, sigma, R, eta): 
        def func_r0(r0, xi_0, SIR_threshold, G, sigma, R, eta):
            f = (2*r0/R**2)*G*np.exp(-G*(Integral_xi(r0, xi_0, SIR_threshold, sigma, R, eta)))
            return f
        args = (xi_0, SIR_threshold, G, sigma, R, eta)
        int = Quad(func_r0, 0, 1, args)
        return int
    
    def Integral_xi0(SIR_threshold, G, sigma, R, eta): 
        def func_xi0(xi_0, SIR_threshold, G, sigma, R, eta):
            f = Integral_r0(xi_0, SIR_threshold, G, sigma, R, eta)
            return f
        args = (SIR_threshold, G, sigma, R, eta)
        int = GaussQuad(func_xi0, sigma, args)
        return int
    
    def CPIntegral_r0(xi_0, SIR_threshold, G, sigma, R, eta, n): 
        def CPfunc_r0(r0, xi_0, SIR_threshold, G, sigma, R, eta, n):
            f = 1- Integral_xi(r0, xi_0, SIR_threshold, sigma, R, eta)
            return f**(n-1)*n*2*r0/R**2
        args = (xi_0, SIR_threshold, G, sigma, R, eta, n)
        int = Quad(CPfunc_r0, 0, R, args)
        return int

    def CPIntegral_xi0(SIR_threshold, G, sigma, R, eta, n): 
        def CPfunc_xi0(xi_0, SIR_threshold, G, sigma, R, eta, n):
            f = CPIntegral_r0(xi_0, SIR_threshold, G, sigma, R, eta, n)
            return f
        args = (SIR_threshold, G, sigma, R, eta, n)
        int = GaussQuad(CPfunc_xi0, sigma, args)
        return int

    capture_prob = [CPIntegral_xi0(SIR_threshold, G, sigma, R, eta, n) for n in collision_size]

    Ps = Integral_xi0(SIR_threshold, G, sigma, R, eta)
    r = {'success_prob': Ps, 'failure_prob': 1-Ps, 'capture_prob': capture_prob}
    return r

