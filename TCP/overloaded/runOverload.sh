./waf
export NS_LOG= #clear the log variable
./waf --run "scratch/tcp_overloaded --DataRateR1=400 --DataRateR2=400 --DataRateR3=100 --DataRateR4=100 --DataRateC1=1000 --DataRateC2=10000 --DataRateC3=200"