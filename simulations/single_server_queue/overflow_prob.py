import numpy as np
from single_server import queue
import matplotlib.pyplot as plt
import seaborn as sns

def bisection(f, a, b, tol=1e-5):#tolerance is on buffer size
    fa = f(a)
    fb = f(b)
    if fa*fb > 0:
        raise ValueError("f(a) and f(b) must have different sign")
    c = a
    while b-a > tol:
        c = int((a+b)/2)
        fc = f(c)
        if np.abs(fc) <= tol:
            return c
        if fa*fc < 0:
            b = c
        else:
            a = c
    return c

def main ():
    # ###############################################################################
    #                        UNITARY SERVICE TIME                                 #
    # ###############################################################################
    print ("\n\nUNITARY SERVICE TIME ")
    # find the queue size for which P[overflow]=0.001 for a=1/4

    def f1(buffer_size):
        np.random.seed(0)
        r = queue(1, 0.5, 0.25, 0.25, buffer_size=buffer_size, verbose=False)
        print (f"buffer_size={buffer_size}, P[overflow]={r['overflow_prob']}")
        return (r['overflow_prob']-0.001)

    #its a root finding problem: find the buffer size for which P[overflow]=0.001
    res = bisection(f1, 1, 1000, tol=4e-4)
    np.random.seed(0)
    r = queue(1, 0.5, 0.25, 0.25, buffer_size=res, verbose=False)
    print("\np(0)=0.5, p(1)=0.25, p(2)=0.25, Buffer size {}, corresponding probability {:.3f}\n".format(res, r['overflow_prob']))

    def f2(buffer_size):
        np.random.seed(0)
        r = queue(1, 1/3, 1/3, 1/3, buffer_size=buffer_size, verbose=False)
        print (f"buffer_size={buffer_size}, P[overflow]={r['overflow_prob']}")
        return (r['overflow_prob']-0.001)

    #its a root finding problem: find the buffer size for which P[overflow]=0.001
    res = bisection(f2, 1, 100000, tol=4e-4)
    np.random.seed(0)
    r = queue(1, 1/3, 1/3, 1/3, buffer_size=res, verbose=False)
    print("\np(0)=0.33, p(1)=0.33, p(2)=0.33, Buffer size {}, corresponding probability {:.3f}\n".format(res, r['overflow_prob']))


    # ###############################################################################
    #                        GEOMETRIC SERVICE TIME                                 #
    # ###############################################################################
    print ("\nGEOMETRIC SERVICE TIME ")
    # find the queue size for which P[overflow]=0.001 for b=2/3

    def g1(buffer_size):
        buffer_size = int(buffer_size)
        np.random.seed(0)
        r = queue(2/3, 0.5, 0.5, 0, service_time='geometric', buffer_size=buffer_size, verbose=False)
        print (f"buffer_size={buffer_size}, P[overflow]={r['overflow_prob']}")
        return (r['overflow_prob']-0.001)
    
    #its a root finding problem: find the buffer size for which P[overflow]=0.001
    res = bisection(g1, 1, 10000, tol=5e-4)
    np.random.seed(0)
    r = queue(2/3, 0.5, 0.5, 0, service_time='geometric', buffer_size=res, verbose=False)
    print("\nb = 2/3, Buffer size {}, corresponding probability {:.3f}\n".format(res, r['overflow_prob']))

    def g2(buffer_size):
        buffer_size = int(buffer_size)
        np.random.seed(0)
        r = queue(1/2, 0.5, 0.5, 0, service_time='geometric', buffer_size=buffer_size, verbose=False)
        print (f"buffer_size={buffer_size}, P[overflow]={r['overflow_prob']}")
        return (r['overflow_prob']-0.001)
    
    #its a root finding problem: find the buffer size for which P[overflow]=0.001
    res = bisection(g2, 1, 10000, tol=5e-4)
    np.random.seed(0)
    r = queue(1/2, 0.5, 0.5, 0, service_time='geometric', buffer_size=res, verbose=False)
    print("\n\nb=1/2 Buffer size {}, corresponding probability {:.3f}\n".format(res, r['overflow_prob']))
    
if __name__ == "__main__":
    main()