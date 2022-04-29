import numpy as np
from single_server import queue
import matplotlib.pyplot as plt
import seaborn as sns

def main ():

    ###############################################################################
    #                        UNITARY SERVICE TIME                                 # 
    ###############################################################################
    print ("\n\nUNITARY SERVICE TIME ")
    print("\nPlot delay vs. utilization factor rho by varying a from 0 to 1/3;")
    # Plot delay vs. utilization factor rho by varying a from 0 to 1/3; 
    a = [1/i for i in range(3,12)]
    avg_throughput = []
    avg_delay = []
    avg_occupancy = []
    rho = []
    np.random.seed(0)

    for aa in a:
        r = queue(1, 1-2*aa, aa, aa)
        avg_throughput.append(r['avg_throughput'])
        avg_delay.append(r['avg_delay'])
        avg_occupancy.append(r['avg_occupancy'])
        rho.append(r['rho'])

    sns.set_theme(style="white", font_scale=2, palette = "Dark2")
    fig, ax = plt.subplots(figsize=(10,6))
    for i in range(len(a)):
        # print(f"a={a[i]}, avg_throughput={avg_throughput[i]}, avg_delay={avg_delay[i]}, avg_occupancy={avg_occupancy[i]}, rho={rho[i]}")
        ax.scatter(x=avg_delay[i], y=rho[i], label="a={:.2f}".format(a[i]), linewidth=0, marker="o", s=100)

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), borderaxespad=0.)
    ax.set_xlabel("Average delay")
    ax.set_ylabel(r"Utilization factor $\rho$")
    fig.savefig(f"figures/delay_vs_rho_fixedtime.png", bbox_inches='tight')

    print ("\nplot a realization of queue size vs time for 10000 slots for a=1/4 ,1/3 and 1/2 and comment.")
    # plot a realization of queue size vs time for 10000 slots for a=1/4 ,1/3 and 1/2 and comment.
    a = [1/4, 1/3, 1/2]
    histories = []
    T = 10000
    np.random.seed(0)
    for aa in a:
        r = queue(1, 1-2*aa, aa, aa, maxtime=T)
        print("Rho {:.2f}".format(r['rho']))
        histories.append(r['history_state'])

    sns.set_theme(style="white", font_scale=2, palette = "Dark2")
    for aa in a:
        fig, ax = plt.subplots(figsize=(18,6))

        sns.lineplot(x=range(T), y=histories[a.index(aa)], color='crimson',
                    linewidth=2, marker="o", markersize=0)

        ax.set_xlabel("Time [slot]")
        ax.set_ylabel(r"Users in the system")
        fig.savefig("figures/queue_size_vs_time_a={:.2f}.png".format(aa), bbox_inches='tight')   


    ###############################################################################
    #                         GEOMETRIC SERVICE TIME                           #
    ###############################################################################
    print ("\n\nGEOMETRIC SERVICE TIME ")
    # P[1 arrival]=1-P[0 arrivals]=0.5, service time for each arrival is a geometric number of slots with mean 1/b. 
    # Plot delay vs. rho by varying b from 0.5 to 1; 
    print("\nPlot delay vs. rho by varying b from 0.5 to 1; " )
    p_one = 0.5
    p_two = 0
    p_zero = 0.5
    b = [0.5, 0.6, 0.7, 0.8, 0.9, 1]

    results = []
    np.random.seed(0)
    for bb in b:
        r = queue(bb, p_zero, p_one, p_two, service_time='geometric')
        results.append(r)

    sns.set_theme(style="white", font_scale=2, palette = "Dark2")
    fig, ax = plt.subplots(figsize=(10,6))
    for i in range(len(b)):
        ax.scatter(x=results[i]['avg_delay'], y=results[i]['rho'], label="b={:.2f}".format(b[i]), linewidth=0, marker="o", s=100)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), borderaxespad=0.)
    ax.set_xlabel("Average delay")
    ax.set_ylabel(r"Utilization factor $\rho$")
    fig.savefig(f"figures/delay_vs_rho_geometric.png", bbox_inches='tight')

    print("\nplot a realization of queue size vs time for 10000 slots for b=1/3, 1/2, 2/3;")
    # plot a realization of queue size vs time for 10000 slots for b=1/3, 1/2, 2/3;
    p_one = 0.5
    p_two = 0
    p_zero = 0.5
    b = [1/3, 1/2, 2/3]
    T = 10000
    np.random.seed(0)

    histories = []
    for bb in b:
        r = queue(bb, p_zero, p_one, p_two, service_time='geometric', maxtime=T)
        histories.append(r['history_state'])

    sns.set_theme(style="white", font_scale=2, palette = "Dark2")
    for bb in b:
        fig, ax = plt.subplots(figsize=(18,6))
        sns.lineplot(x=range(T), y=histories[b.index(bb)], color='crimson',
                    linewidth=2, marker="o", markersize=0)

        ax.set_xlabel("Time [slot]")
        ax.set_ylabel(r"Users in the system")
        fig.savefig("figures/queue_size_vs_time_b={:.2f}.png".format(bb), bbox_inches='tight')

if __name__ == '__main__':
    main()
    print("Done!")