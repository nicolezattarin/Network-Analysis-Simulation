import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def func(size=None):
        """
        e^U, U~U(0,1)
        returns:
        e^u, e^(1-U), U
        """

        if size == None or size == 1:
            U = np.random.uniform()
            rand1 = np.exp(U)
            rand2 = np.exp(U)
        else:
            size = int(size)
            rand1 = np.zeros(size)
            rand2 = np.zeros(size)
            U = np.random.uniform(size=size)
            for i in range(size):
                rand1[i] = np.exp(U[i])
                rand2[i] = np.exp(1-U[i])
        return rand1, rand2, U

def control_variates(X, Y):
    cov = np.cov(X, Y)[0][1]
    varY = np.var(Y)
    varX = np.var(X)
    c = -cov/varY
    muY = np.mean(Y)
    newvars = X+c*(Y-muY)
    var_observed = np.var(newvars) 
    var_computed = varX - cov**2/varY
    print ('\n\nVariance computed by control variates: {:.3f}'.format(var_computed))
    print ('Variance observed: {:.3f}'.format(var_observed))
    print ('Original variance: {:.3f}'.format(varX))
    print ('Variance difference: {:.3f}'.format(var_computed-varX))
    print ('Mean of new variable: {:.3f}'.format(np.mean(newvars)))
    print ('Mean of original variable: {:.3f}'.format(np.mean(X)))
    print ('c: {:.3f}'.format(c))
    print ('cova: {:.3f}'.format(cov))
    return newvars

def antithetic_variables (X, Y):
    # variance of each sequence
    var1 = np.var(seq1)
    var2 = np.var(seq2)
    print('\n\nVariance of the first sequence: {:.3f}'.format(var1))
    print('Variance of the second sequence: {:.3f}'.format(var1))

    #apply antithetic variables
    seq = [(v1+v2)/2. for v1, v2 in zip(seq1, seq2)]
    var = np.var(seq)
    print('Variance of the sequence with antithetic variables: {:.3f}'.format(var))
    
    # other statistics
    print('Mean of the first sequence: {:.3f}'.format(np.mean(seq1)))
    print('Mean of the second sequence: {:.3f}'.format(np.mean(seq2)))
    print('Covariance of the first-second sequence: {:.3f}'.format(np.cov(seq1, seq2)[0][1]))
    return seq

###############################################################################
#                        ANTITHETIC VARIABLES                                 #
###############################################################################
N=1000

seq1, seq2, _ = func(size=N)
newvars_AV = antithetic_variables (seq1, seq1) 


###############################################################################
sns.set_theme(style='white', palette='Dark2', font_scale=2)
fig, ax = plt.subplots(figsize=(15,6))
covmat = np.cov(seq1, seq2)

lw = 3
ax.plot(seq1, lw=lw, label =r'$e^{U}$')
ax.plot(seq2, lw=lw, label = r'$e^{1-U}$')
ax.plot(newvars_AV, lw=4, label = r'$(e^{U}+e^{1-U})/2$')

ax.set_xlim(0,50)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.8))
ax.set_xlabel('index')
ax.set_ylabel('data')
fig.savefig('trend_AV.pdf', bbox_inches='tight')

###############################################################################
sns.set_theme(style='white', palette='Dark2', font_scale=2)
fig, ax = plt.subplots(1,3, figsize=(15,6))
covmat = np.cov(seq1, seq2)

lw = 3
sns.histplot(seq1,label =r'$e^{U}$', ax=ax[0], stat='density',alpha=0.5,edgecolor=None)
sns.histplot(seq2, lw=lw, label = r'$e^{1-U}$', ax=ax[1], stat='density', alpha=0.5,edgecolor=None)
sns.histplot(newvars_AV, lw=lw, label = r'$e^{1-U}$', ax=ax[2], stat='density',alpha=0.5,edgecolor=None)
#mean and var
ax[0].axvline(x=np.mean(seq1), lw=3, color='black')
ax[1].axvline(x=np.mean(seq2), lw=3, color='black')
ax[2].axvline(x=np.mean(newvars_AV), lw=3, color='black')
ax[0].axvline(x=np.mean(seq1)+np.var(seq1), lw=3, color='black', linestyle='--')
ax[1].axvline(x=np.mean(seq2)+np.var(seq2), lw=3, color='black', linestyle='--')
ax[2].axvline(x=np.mean(newvars_AV)+np.var(newvars_AV), lw=3, color='black', linestyle='--')
ax[0].axvline(x=np.mean(seq1)-np.var(seq1), lw=3, color='black', linestyle='--')
ax[1].axvline(x=np.mean(seq2)-np.var(seq2), lw=3, color='black', linestyle='--')
ax[2].axvline(x=np.mean(newvars_AV)-np.var(newvars_AV), lw=3, color='black', linestyle='--')

ax[0].set_ylabel('density'), ax[1].set_ylabel(''),ax[2].set_ylabel('')
ax[0].set_xlabel('data'), ax[1].set_xlabel('data'), ax[2].set_xlabel('data')
ax[0].set_ylim(0,1), ax[1].set_ylim(0,1),ax[2].set_ylim(0,1)
ax[0].set_xlim(0.9,2.8), ax[1].set_xlim(0.9,2.8),ax[2].set_xlim(1.5,2)
ax[0].set_title(r'$e^{U}$'), ax[1].set_title(r'$e^{1-U}$'), ax[2].set_title(r'$(e^{U}+e^{1-U})/2$')
fig.savefig('distr_AV.pdf', bbox_inches='tight')


###############################################################################
#                        CONTROL VARIATES                                    #
###############################################################################

seq, _, U = func(size=N)
newvars_CV = control_variates(seq, U)

###############################################################################
sns.set_theme(style='white', palette='Dark2', font_scale=2)
fig, ax = plt.subplots(figsize=(10,6))
covmat = np.cov(seq1, seq2)

lw = 3
ax.plot(seq, lw=lw, label =r'$e^{U}$')
ax.plot(newvars_CV, lw=4, label = r'$e^{U}+c(U-\mu_U)$')

ax.set_xlim(0,50)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.8))
ax.set_xlabel('index')
ax.set_ylabel('data')
fig.savefig('trend_CV.pdf', bbox_inches='tight')

###############################################################################
sns.set_theme(style='white', palette='Dark2', font_scale=2)
fig, ax = plt.subplots(1,2, figsize=(10,6))

lw = 3
sns.histplot(seq,label =r'$e^{U}$', ax=ax[0], stat='density',alpha=0.5,edgecolor=None)
sns.histplot(newvars_CV, lw=lw, label = r'$e^{1-U}$', ax=ax[1], stat='density',alpha=0.5,edgecolor=None)
#mean and var
ax[0].axvline(x=np.mean(seq), lw=3, color='black')
ax[1].axvline(x=np.mean(newvars_CV), lw=3, color='black')
ax[0].axvline(x=np.mean(seq)+np.var(seq), lw=3, color='black', linestyle='--')
ax[1].axvline(x=np.mean(newvars_CV)+np.var(newvars_CV), lw=3, color='black', linestyle='--')
ax[0].axvline(x=np.mean(seq)-np.var(seq), lw=3, color='black', linestyle='--')
ax[1].axvline(x=np.mean(newvars_CV)-np.var(newvars_CV), lw=3, color='black', linestyle='--')

ax[0].set_ylabel('density'), ax[1].set_ylabel('')
ax[0].set_xlabel('data'), ax[1].set_xlabel('data')
ax[0].set_ylim(0,1), ax[1].set_ylim(0,1)
ax[0].set_xlim(0.9,2.8), ax[1].set_xlim(1.6,1.9)
ax[0].set_title(r'$e^{U}$'), ax[1].set_title(r'$e^{U}+c(U-\mu_U)$')
fig.savefig('distr_CV.pdf', bbox_inches='tight')