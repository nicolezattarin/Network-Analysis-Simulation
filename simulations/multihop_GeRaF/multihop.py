import numpy as np

class point ():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def distance(self, other):
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class node():
    def __init__(self, x, y, active):
        self.position = point(x, y)
        self.active = active
    def distance(self, point):
        return np.sqrt((self.position.x - point.x)**2 + (self.position.y - point.y)**2)

def make_hop(node_list, current_node, activation_prob, destination):
    # select nodes within the current node's range (distance <= 1)
    range_nodes = [node for node in node_list if node.distance(current_node.position) <= 1]
    # make nodes active with probability activation_prob
    for node in range_nodes:
        if np.random.uniform() < activation_prob:
            node.active = True
    active_nodes = [node for node in range_nodes if node.active]
    # check if there are any active nodes
    if len(active_nodes) == 0:
        return current_node

    #select the active node closest to the destination
    distances = [node.distance(destination) for node in active_nodes]
    new_current = active_nodes[np.argmin(distances)]
    return new_current

def avg_hops(node_density, activation_prob, destination, start_position, verbose=False):
    """
    args: 
        node_density: number of nodes in the network/area
        activation_prob: probability of a node being active
        destination: point object representing the destination
        start_position: point object representing the starting node
    """
    if verbose:
        print("\n\nnode density:", node_density)
        print("activation prob:", activation_prob)
        print("destination:", destination.x, destination.y)
        print("start position:", start_position.x, start_position.y)
        
    nhops = 0
    # define an area to put the nodes, assuming to strart at (distance,0), target is (0,0)
    # define a recngle with corners in (-1, -1) and (distance+1, distance+1)
    distance = destination.distance(start_position)
    tolerance = 1
    if start_position.x < destination.x: # if the start node is to the left of the destination
        x_min = start_position.x - tolerance
        x_max = destination.x + tolerance
    else: # if the start node is to the right of the destination
        x_min = destination.x - tolerance
        x_max = start_position.x + tolerance
    if start_position.y < destination.y: # if the start node is above the destination
        y_min = start_position.y - tolerance
        y_max = destination.y + tolerance
    else: # if the start node is below the destination
        y_min = destination.y - tolerance
        y_max = start_position.y + tolerance

    area = (x_max - x_min) * (y_max - y_min)
    # create a list of nodes
    node_list = [node(np.random.uniform(x_min, x_max), np.random.uniform(y_min, y_max), False) for i in range(int(area * node_density))]
    # select the first node
    current_node = node(start_position.x, start_position.y, True)
    if current_node in node_list: 
        node_list.remove(current_node)
        print("start node is in node list")

    # loop until the destination is reached
    while current_node.distance(destination) > 1:
        current_node = make_hop(node_list, current_node, activation_prob, destination)
        nhops += 1
        # if the destination cannot be reached resample (if the number of hops is greater than the number of nodes)
        if nhops > int(area * node_density): 
            node_list = [node(np.random.uniform(x_min, x_max), np.random.uniform(y_min, y_max), False) for i in range(int(area * node_density))]
            current_node = node(start_position.x, start_position.y, True)
            nhops = 0
    
    return nhops

