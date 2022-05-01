./waf
# Set the log level for the given component to info, i.e. run the code and print that level of log
export NS_LOG=log_example=info 
./waf --run scratch/UdpEchoClientServer
# Run with logging system : log component is prefixed with component name and simulation time
export 'NS_LOG=UdpEchoClientApplication=level_all|prefix_func|prefix_time:UdpEchoServerApplication=level_all|prefix_func|prefix_time'
./waf --run scratch/UdpEchoClientServer
# generalization to multiple components is trivial
# informations about every element of the simulation can be printed with
# export 'NS_LOG=*=level_all|prefix_func|prefix_time'

./waf --run "scratch/UdpEchoClientServer --PrintHelp" #to print all possible options for the application
#returns something like this:
# General Arguments:
#     --PrintGlobals:              Print the list of globals.
#     --PrintGroups:               Print the list of groups.
#     --PrintGroup=[group]:        Print all TypeIds of group.
#     --PrintTypeIds:              Print all TypeIds.
#     --PrintAttributes=[typeid]:  Print all attributes of typeid.
#     --PrintHelp:                 Print this help message.

# e.g. ./waf --run "scratch/UdpEchoClientServer --PrintAttributes=ns3::PointToPointNetDevice"
# e.g. ./waf --run "scratch/UdpEchoClientServer --PrintAttributes=ns3::PointToPointChannel"

# we can set values from command line
# ./waf --runn "scratch/UdpEchoClientServer --ns3::PointToPointNetDevice::DataRate=5Mbps --ns3::PointToPointChannel::Delay=2ms"
