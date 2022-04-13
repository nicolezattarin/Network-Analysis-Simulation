import pandas as pd
import numpy as np

""" 
In discrete-event (event-driven) simulation, time is not scanned regularly, but we jump from one event to the next
- Good features: no time is wasted while no events, can model most systems of interest
- More difficult to program: need to manage time, events, counters
- When an event occurs: update time, update counters, execute event, generate future
 events and put them in the event calendar (if any), modify current events (if any)


Our model:
- Bernoulli arrivals: 1 with probability a
- Geometric service times: 1 with probability b (depart only if there are users in the system)
- memoryless system: no memory of past events
- Arrivals cannot depart and leave in the same slot

Variables:
- time t: current time
- number of users n_system: number of users in the system
- number of arrivals n_arrivals: number of arrivals in the system
- number of departures n_departures: number of departures in the system
- total cumulative delay cum_delay: cumulative delay of all users
- total cumulative number of users cum_n_system: cumulative number of users in the system

"""
def FIFO (dep_prob, arr_prob, maxtime=1000):
    t, n_system, n_arrivals, n_departures = 0,0,0,0 # t count the slot
    cum_delay, cum_n_system = 0,0  

    # we consider a slotted time and simulate what happens in the slot
    while t<maxtime:
        # if there are users in the system, consider departure probability
        if n_system > 0:
            cum_n_system+=n_system #accumulate the number of users in the system
            u = np.random.uniform()
            if u < dep_prob:
                n_departures+=1
                n_system-=1
        u = np.random.uniform()
        if u < arr_prob:
            n_arrivals+=1
            n_system+=1
        t+=1
    avg_throughput = n_departures/maxtime #how many users has been served in the system
    avg_delay = cum_n_system/n_departures
    avg_occupancy = cum_n_system/maxtime
    return avg_throughput, avg_delay, avg_occupancy