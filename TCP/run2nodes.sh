./waf
export NS_LOG= #clear the log variable
./waf --run scratch/tcp2nodes  > cwnd.dat 2>&1