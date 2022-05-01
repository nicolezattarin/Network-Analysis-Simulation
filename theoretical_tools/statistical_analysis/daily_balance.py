import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def main():
    balance = np.loadtxt('data/figure 2.10/joe.dat')

    #line plot
    fig,ax=plt.subplots(figsize=(10,5))
    sns.set_theme(style='white',palette='Dark2',font_scale=2)
    ls='solid'
    sns.lineplot(x=np.arange(len(balance)), y=balance, linestyle=ls, ax=ax, linewidth=2.5)
    ax.set_ylabel("Daily balance")
    ax.set_xlabel("day")
    ax.set_title("Daily balance at Joe's shop")
    fig.savefig('figs/joe_lineplot.pdf', bbox_inches='tight')

    #lag plots
    df = pd.DataFrame(np.zeros((len(balance),10)), columns=['balance',*['lag_{}'.format(i) for i in range(1,10)]])
    df.loc[:, 'balance'] = balance
    for i in range(1,10):
        df.loc[:, 'lag_{}'.format(i)] = df['balance'].shift(periods=i)
    df = df.dropna()
    df.index = np.arange(len(df))

    fig,ax=plt.subplots(3,3,figsize=(22,20))
    sns.set_theme(style='white',palette='Dark2',font_scale=2)

    for i in range(9):
        sns.scatterplot(y='balance', x='lag_{}'.format(i+1), data=df, ax=ax[i//3,i%3], color='teal', s=70)
        ax[i//3,i%3].set_xlabel("y(t+{})".format(i+1))
        if i%3==0:
            ax[i//3,i%3].set_ylabel("y(t)")
        else: ax[i//3,i%3].set_ylabel("")
    fig.savefig('figs/joe_lag_plots.pdf', bbox_inches='tight')

    #autocorrelation plots
    fig,ax=plt.subplots(figsize=(10,5))
    from statsmodels.graphics import tsaplots
    tsaplots.plot_acf(balance, lags=90, ax=ax,zero=False)
    ax.set_xlabel("lag")
    ax.set_ylabel("Correlation")
    fig.savefig('figs/joe_autocorr.pdf', bbox_inches='tight')

if __name__ == '__main__':
    main()
        