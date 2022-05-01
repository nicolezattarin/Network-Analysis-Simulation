import numpy as np

def queue (dep_prob, 
            zero_arr_prob, 
            one_arr_prob, 
            two_arr_prob, 
            maxtime=10000, 
            service_time='unitary', 
            verbose=True,
            buffer_size=int(1e8)):
    """
    Simulates a queue with a single server.
    Parameters
    ----------
    dep_prob: float
        Probability of a departure.
    zero_arr_prob: float
        Probability of an arrival of 0.
    one_arr_prob: float
        Probability of an arrival of 1.
    two_arr_prob: float
        Probability of an arrival of 2.
    maxtime: int
        Maximum time of the simulation.
    service_time: str
        Service time of the server.
    verbose: bool
        If True, prints the results.
    buffer_size: int
        Size of the buffer, i.e. the maximum number of users in the system.

    Returns
    -------
    results: dict
        Dictionary with the results.
    """
    t, n_system, n_arrivals, n_departures = 0,0,0,0 # t count the slot
    cum_n_system = 0
    history_state = []
    none = 0
    ntwo = 0
    n_dropped = 0 #dropped because of buffer overflow

    if dep_prob < 0 or dep_prob > 1: raise ValueError("dep_prob must be between 0 and 1")
    if one_arr_prob < 0 or one_arr_prob > 1: raise ValueError("one_arr_prob must be between 0 and 1")
    if two_arr_prob < 0 or two_arr_prob > 1: raise ValueError("two_arr_prob must be between 0 and 1")
    if zero_arr_prob < 0 or zero_arr_prob > 1: raise ValueError("zero_arr_prob must be between 0 and 1")
    if zero_arr_prob + one_arr_prob + two_arr_prob != 1: raise ValueError("zero_arr_prob + one_arr_prob + two_arr_prob must be 1")
    
    if verbose:
        print ("\n\ndep_prob:{:.2f}, zero_arr_prob: {:.2f}, one_arr_prob: {:.2f}, two_arr_prob: {:.2f}".\
            format(dep_prob, zero_arr_prob, one_arr_prob, two_arr_prob))

    # we consider a slotted time and simulate what happens in the slot
    # geometric service time
    if service_time == 'geometric':
        st = np.random.geometric(dep_prob)
        if verbose: print('service time:', st)
    service_times = [] 
    arrival_times = []
    while t<maxtime:
        # if there are users in the system, consider departure probability
        if n_system > 0:
            cum_n_system+=n_system #accumulate the number of users in the system
            u = np.random.uniform(0,1)
            if service_time == 'geometric':
                st -= 1
                if st == 0:
                    n_departures += 1
                    n_system -= 1
                    st = np.random.geometric(dep_prob)
                    service_times.append(st)
            elif service_time == 'unitary':
                if u < dep_prob:
                    n_departures+=1
                    n_system-=1
                    service_times.append(1)
        u = np.random.uniform()
        if u < one_arr_prob:
            if n_system == buffer_size:
                n_dropped+=1
                history_state.append(n_system)
                t+=1
                continue
            n_arrivals+=1
            n_system+=1
            none += 1
            arrival_times.append(1) #time is unitary so we don't divide by 1
        elif one_arr_prob<u and u<one_arr_prob+two_arr_prob:
            if n_system == buffer_size:
                n_dropped+=2
                history_state.append(n_system)
                t+=1
                continue
            n_arrivals+=2
            n_system+=2
            ntwo += 1
            arrival_times.append(2) #time is unitary so we don't divide by 1
        else:
            arrival_times.append(0) #time is unitary so we don't divide by 1

        history_state.append(n_system)
        t+=1

    avg_throughput = n_departures/maxtime #how many users has been served in the system
    avg_delay = cum_n_system/n_departures #average delay
    avg_occupancy = cum_n_system/maxtime

    total_arrivals = np.sum(arrival_times)
    avg_arrival_rate = np.mean(arrival_times)
    avg_service_time = 1/np.mean(service_times)
    rho = avg_arrival_rate/avg_service_time
    overflow_prob = n_dropped/total_arrivals
    # DEBUG
    if verbose:
        print('\np one arrival: {}'.format(none/maxtime))
        print('p two arrivals: {}'.format(ntwo/maxtime))
        print('p zero arrival: {}'.format(1-none/maxtime-ntwo/maxtime))
        print('p departure: {}'.format(dep_prob))
        print('avg_arrival_rate: {}'.format(avg_arrival_rate))
        print('avg_service_time: {}'.format(avg_service_time))
        print ("expected average service time:", 1/dep_prob)
        print('rho: {}'.format(rho))
        print ('overflow_prob: {}'.format(overflow_prob))

    result = {'avg_throughput': avg_throughput,
                'avg_delay': avg_delay,
                'avg_occupancy': avg_occupancy,
                'avg_arrival_rate': avg_arrival_rate,
                'avg_service_time': avg_service_time,
                'rho': rho,
                'history_state': history_state,
                'overflow_prob': overflow_prob,}
    return result