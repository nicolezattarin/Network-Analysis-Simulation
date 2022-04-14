import numpy as np
from simulations import FIFO

def main():

    # simple queue simulation

    arr_probs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    dep_probs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    throughputs = np.zeros((len(arr_probs),len(arr_probs)), dtype=float)
    delays = np.zeros((len(arr_probs),len(arr_probs)), dtype=float)
    occupancies = np.zeros((len(arr_probs),len(arr_probs)), dtype=float)
    for a in range(len(arr_probs)) :
        for d in range(len(dep_probs)) :
            throughputs[a,d], delays[a,d], occupancies[a,d] = FIFO(dep_probs[d], arr_probs[a])

    import os
    os.makedirs('data', exist_ok=True)

    np.savetxt("data/throughputs.csv", throughputs, delimiter=",")
    np.savetxt("data/delays.csv", delays, delimiter=",")
    np.savetxt("data/occupancies.csv", occupancies, delimiter=",")

if __name__ == "__main__":
    main()