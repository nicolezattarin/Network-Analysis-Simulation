import numpy as np

# the area is divided into square grids of side r = sqrt (5) (normalized to radio coverage). 
# In the best case (they are parallel), one hop leads to an advancement of r units toward the destination,
# whereas, in the worst case hop advancement is r= sqrt(10) 
def best_case(distance):
    return distance * np.sqrt(5)

def worst_case(distance):
    return distance * np.sqrt(10)

