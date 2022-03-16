import numpy as np
import argparse
import matplotlib.pyplot as plt
import seaborn as sns

def stat_sim(N, distr, level=0.95, verbose=False):
    """
    This function generates N data and calculate the mean, the standard deviation and the
    confidence interval of the mean.
    """
    # Generate N iid RVs
    if distr == "unif":
        data = np.random.uniform(0, 1, N)
    elif distr == "norm":
        data = np.random.normal(0, 1, N)
    
    # Calculate mean and standard deviation
    mean = np.mean(data)
    std = np.std(data)

    from scipy.stats import norm
    # Calculate confidence interval
    eta = np.abs(norm.ppf((1-level)/2))
    
    mean_plus = mean+std/np.sqrt(N)*eta
    mean_minus = mean-std/np.sqrt(N)*eta

    from scipy.stats import chi2
    a = chi2.ppf((1-level)/2, N-1)
    b = chi2.ppf((1+level)/2, N-1)
    std_low = std*np.sqrt(a/(N-1))
    std_high = std*np.sqrt(b/(N-1))
    
    if verbose: 
        print("The mean is {:.2f} and the standard deviation is {:.2f}.".format(mean, std))
        print("The CI of the mean for level = {:.2f} is [{:.2f}, {:.2f}].".format(level, mean_minus, mean_plus))
        print("The CI of the std for level = {:.2f} is [{:.2f}, {:.2f}].".format(level, std_low, std_high))
    return mean, std, mean_minus, mean_plus, std_low, std_high

def main():

    """
    UNIFORM DISTRIBUTION
    """
    # np.random.seed(0)

    print("\nUNIFORM DISTRIBUTION")
    # simulation with 48 iid unif(0,1)
    unif_mean, unif_std, unif_mean_minus, unif_mean_plus, _, _ = stat_sim(N=48, distr="unif")
    print('simulation with 48 iid unif(0,1)')
    print('mean: {:.2f}'.format(unif_mean))
    print('std: {:.2f}'.format(unif_std))
    print('CI: [{:.2f}, {:.2f}]'.format(unif_mean_minus, unif_mean_plus))

    # Repeat the experiment independently for 1000 times
    print("\nRepeat the experiment independently for 1000 times")
    n_it = 1000
    import pandas as pd
    unif_df = pd.DataFrame(np.zeros(shape=(n_it,4)), columns=["mean", "std", "mean_low", "mean_up"])
    for i in range(n_it): 
        unif_mean, unif_std, unif_mean_minus, unif_mean_plus, _, _ = stat_sim(N=48, distr="unif")
        unif_df.iloc[i,:] = [unif_mean, unif_std, unif_mean_minus, unif_mean_plus]
    # find how many times the confidence interval does not contain the TRUE VALUE of the mean;
    n_errors = 0
    truemean = 0.5
    for low, up in zip(unif_df["mean_low"], unif_df["mean_up"]):
        if truemean < low or truemean > up: n_errors += 1
    print("Observed probability of error {:.2f}.".format(n_errors/n_it))

    #distribution of the mean plot
    fig,ax=plt.subplots(figsize=(10,6))
    sns.set_theme(style='white',palette='Dark2',font_scale=1.5)
    sns.histplot(x='mean', data=unif_df, color='darkorange', bins=30, alpha=1, label='Mean')
    ax.axvline(x=0.5, color='black', linestyle='--', label='True mean', linewidth=3)
    ax.legend(loc='upper left')
    fig.savefig('figs/mean_distr_unif.png', bbox_inches='tight')

    #plot the results ordering the intervals by increasing lower extreme of the CI
    unif_df.sort_values(by='mean_low', inplace=True)
    fig,ax=plt.subplots( figsize=(10,6))
    for lower, upper, y in zip(unif_df['mean_low'],unif_df['mean_up'], range(len(unif_df))):
        ax.plot((lower,upper), (y,y),'ro-',color='darkorange', alpha=0.5)
    ax.plot((lower,upper), (y,y),'ro-',color='darkorange', alpha=0.5, label='CI')
    ax.plot(unif_df['mean'], range(len(unif_df)),'ro',color='teal', alpha=0.9, label = 'Mean')
    ax.axvline(x=0.5, color='black', linestyle='--', label='True mean', linewidth=3)
    ax.legend(loc='upper left')
    ax.set_yticklabels('')
    ax.set_xlabel('Mean')
    fig.savefig('figs/unif_mean_CI.png', bbox_inches='tight')

    # Generate n iid U(0,1) r.v.’s, and compute sample mean and sample variance
    print ('\nSimulation with n iid U(0,1) r.v.')
    nmax = 1000
    ns = np.arange(1,nmax+1, 20)
    N_df_unif = pd.DataFrame(np.zeros(shape=(len(ns),7)), columns=["N", "mean", "std", "mean_low", "mean_up", "std_low", "std_up"] )
    for i in range(len(ns)):
        np.random.seed(0)
        N_df_unif.iloc[i,:]=np.concatenate([[ns[i]], stat_sim(N=ns[i], distr="unif")])

    # Study the accuracy of the estimate with respect to the true value vs. n
    N_df_unif['mean_accuracy'] = np.log10(1/abs(N_df_unif['mean']-0.5))
    fig,ax=plt.subplots(figsize=(10,6))
    lw=2
    ms=8
    ls='--'
    g=sns.lineplot(x='N', y='mean_accuracy', ax=ax, data=N_df_unif, marker='o', 
                    markersize=ms,linewidth=lw, linestyle=ls)

    g.legend(loc='center left', bbox_to_anchor=(1, 0.5), borderaxespad=0.)
    ax.set_ylabel(r"Accuracy $\log_{10}(1/\epsilon)$")
    ax.set_xlabel(r"$N$")
    fig.savefig('figs/unif_mean_accuracy.pdf', bbox_inches='tight')

    # Find confidence intervals for the variance vs. n
    print('\nFind confidence intervals for the VARIANCE vs. n')

    #plot confidence intervals for the variance vs. n
    fig,ax=plt.subplots( figsize=(10,6))
    for lower, upper, y in zip(N_df_unif['std_low'],N_df_unif['std_up'], N_df_unif['N']):
        ax.plot((lower**2,upper**2), (y,y),color='darkorange',linewidth=2)
    ax.plot((lower**2,upper**2), (y,y) ,color='darkorange', alpha=0.5, label='CI', linewidth=2)
    ax.plot(N_df_unif['std']**2, N_df_unif['N'],'ro',color='teal', label = 'STD', markersize=5)
    ax.legend(loc='upper left')
    ax.set_xlabel(r"$\sigma^2$")
    ax.set_ylabel('N')
    ax.set_xlim(0.02,0.145)
    fig.savefig('figs/unif_variance_CI.png', bbox_inches='tight')


    # Find 95% prediction interval using theory and using bootstrap
    print('\nFind 95% prediction interval using theory')


    """
    NORMAL DISTRIBUTION
    """
    np.random.seed(0)
    print('\n\nNORMAL DISTRIBUTION')
    # simulation with 48 iid unif(0,1)
    norm_mean, norm_std, norm_mean_minus, norm_mean_plus, _, _ = stat_sim(N=48, distr="norm")
    print('simulation with 48 iid norm(0,1)')
    print('mean: {:.2f}'.format(norm_mean))
    print('std: {:.2f}'.format(norm_std))
    print('CI: [{:.2f}, {:.2f}]'.format(norm_mean_minus, norm_mean_plus))

    # Repeat the experiment independently for 1000 times
    print("\nRepeat the experiment independently for 1000 times")
    n_it = 1000
    norm_df = pd.DataFrame(np.zeros(shape=(n_it,4)), columns=["mean", "std", "mean_low", "mean_up"] )
    for i in range(n_it): 
        norm_mean, norm_std, norm_mean_minus, norm_mean_plus, _, _ = stat_sim(N=48, distr="norm")
        norm_df.iloc[i,:] = [norm_mean, norm_std, norm_mean_minus, norm_mean_plus]

    # find how many times the confidence interval does not contain the TRUE VALUE of the mean;
    n_errors=0
    truemean=0
    for low, up in zip(norm_df["mean_low"], norm_df["mean_up"]):
        if truemean < low or truemean > up: n_errors += 1
    print("Observed probability of error {:.2f}.".format(n_errors/n_it))

    #distribution of the mean plot
    fig,ax=plt.subplots(figsize=(10,6))
    sns.set_theme(style='white',palette='Dark2',font_scale=1.5)
    sns.histplot(x='mean', data=norm_df, color='darkorange', bins=30, alpha=1, label='Mean')
    ax.axvline(x=truemean, color='black', linestyle='--', label='True mean', linewidth=3)
    ax.legend(loc='upper left')
    fig.savefig('figs/mean_distr_norm.png', bbox_inches='tight')

    #plot the results ordering the intervals by increasing lower extreme of the CI
    norm_df.sort_values(by='mean_low', inplace=True)
    fig,ax=plt.subplots( figsize=(10,6))
    for lower, upper, y in zip(norm_df['mean_low'],norm_df['mean_up'], range(len(norm_df))):
        ax.plot((lower,upper), (y,y),'ro-',color='darkorange', alpha=0.5)
    ax.plot((lower,upper), (y,y),'ro-',color='darkorange', alpha=0.5, label='CI')
    ax.plot(norm_df['mean'], range(len(norm_df)),'ro',color='teal', alpha=0.9, label = 'Mean')
    ax.axvline(x=0, color='black', linestyle='--', label='True mean', linewidth=3)
    ax.legend(loc='upper left')
    ax.set_yticklabels('')
    ax.set_xlabel('Mean')
    fig.savefig('figs/norm_mean_CI.png', bbox_inches='tight')

    # Generate n iid N(0,1) r.v.’s, and compute sample mean and sample variance
    print ('\nSimulation with n iid N(0,1) r.v.')
    N_df_norm = pd.DataFrame(np.zeros(shape=(len(ns),7)), columns=["N", "mean", "std", "mean_low", "mean_up", "std_low", "std_up"] )
    for i in range(len(ns)):
        np.random.seed(0)
        N_df_norm.iloc[i,:]=np.concatenate([[ns[i]], stat_sim(N=ns[i], distr="norm")])

    # Study the accuracy of the estimate with respect to the true value vs. n
    N_df_norm['mean_accuracy'] = np.log10(1/abs(N_df_norm['mean']))
    fig,ax=plt.subplots(figsize=(10,6))
    lw=2
    ms=8
    ls='--'
    g=sns.lineplot(x='N', y='mean_accuracy', ax=ax, data=N_df_norm, marker='o', 
                    markersize=ms,linewidth=lw, linestyle=ls)

    g.legend(loc='center left', bbox_to_anchor=(1, 0.5), borderaxespad=0.)
    ax.set_ylabel(r"Accuracy $\log_{10}(1/\epsilon)$")
    ax.set_xlabel(r"$N$")
    fig.savefig('figs/norm_mean_accuracy.pdf', bbox_inches='tight')

    # Find confidence intervals for the variance vs. n
    print('\nFind confidence intervals for the variance vs. n')

    #plot confidence intervals for the variance vs. n
    fig,ax=plt.subplots( figsize=(10,6))
    for lower, upper, y in zip(N_df_norm['std_low'],N_df_norm['std_up'], N_df_norm['N']):
        ax.plot((lower**2,upper**2), (y,y),color='darkorange',linewidth=2)
    ax.plot((lower**2,upper**2), (y,y) ,color='darkorange', alpha=0.5, label='CI', linewidth=2)
    ax.plot(N_df_norm['std']**2, N_df_norm['N'],'ro',color='teal', label = 'STD', markersize=5)
    ax.legend(loc='upper left')
    ax.set_xlabel(r"$\sigma**2$")
    ax.set_ylabel('N')
    ax.set_xlim(0.25,2)
    fig.savefig('figs/norm_variance_CI.png', bbox_inches='tight')



if __name__ == "__main__":
    main()