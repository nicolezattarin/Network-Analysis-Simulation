from GaussQuadrature import Quad, GaussQuad
import numpy as np

def f(x): return 1
sigma = 1
int = GaussQuad(f, sigma, N=30)
print('numerical ', int)
print ('expected ', np.sqrt(np.pi))

def g(x): return -x**2
int = Quad(g, -2, 2, N=50)
print('numerical ', int)
print ('expected ', -16/3)
