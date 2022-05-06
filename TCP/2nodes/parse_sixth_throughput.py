###############################
# Compute and plot throughput #
###############################

# This script requires the sixth-packets.txt file, which can be
# obtained by running the modified sixth tutorial script. The file
# will be generated in your ns-3 folder.

# Open the file and check it out before executing this script.

# Imports
#########
# Numpy is a library we use to create vectors and matrices that behave very
# similarly to how MATLAB ones do. The "as np" clause in the import lets us
# refer to numpy with the np shorthand name.
import numpy as np
# Matplotlib is the most widely used Python plotting library. This library,
# too, behaves similarly to how MATLAB plots work.
import matplotlib.pyplot as plt

# Data reading
##############

# We use numpy's loadtxt function to import data.
# Reference: https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.loadtxt.html
packets = np.loadtxt('ns-3-dev/sixth-packets.txt')

# Save the time and packet size columns to adequate data structures
t_p = packets[:, 0]
y_p = packets[:, 1]

# Define the data structure to hold our time axis
T = 0.5
t = np.arange(min(t_p),max(t_p), T)

r = np.zeros(len(t))
for i in range(len(t)-1):
    q = np.logical_and(t_p > t[i], t_p < t[i+1]);
    r[i] = np.sum(y_p[q])/T*8/1000000;

# Plotting
##########
plt.figure()
plt.plot(t,r)
plt.title("Throughput")
plt.xlabel("s")
plt.xlabel("MByte")
plt.show()

print("Mean: %s" % np.mean(r))
print("Standard deviation: %s" % np.std(r))
