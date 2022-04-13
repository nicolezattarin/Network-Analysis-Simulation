#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"

// Default Network Topology
//
//       10.1.1.0
// n0 -------------- n1
//    point-to-point
//
 
using namespace ns3;

//  declares a logging component called FirstScriptExample that allows you 
// to enable and disable console message logging by reference to the name.
NS_LOG_COMPONENT_DEFINE ("FirstScriptExample");

int main (int argc, char *argv[])
{
  CommandLine cmd (__FILE__);
  cmd.Parse (argc, argv);
  
  Time::SetResolution (Time::NS); // sets the time resolution to one nanosecond, default value
  // enable debug logging at the INFO level for echo clients and servers. 
  // This will result in the application printing out messages as packets 
  // are sent and received during the simulation.
  LogComponentEnable ("UdpEchoClientApplication", LOG_LEVEL_INFO);
  LogComponentEnable ("UdpEchoServerApplication", LOG_LEVEL_INFO);

  NodeContainer nodes;
  nodes.Create (2);

  PointToPointHelper pointToPoint; // topology helper object to do the low-level work required to 
                                   // put the link together. two of our abstractions are the NetDevice and the Channel.
// the string “DataRate” corresponds to an Attribute of the PointToPointNetDevice. 
// we  are basically setting the values of attributes of our abstractions.
  pointToPoint.SetDeviceAttribute ("DataRate", StringValue ("5Mbps"));
  pointToPoint.SetChannelAttribute ("Delay", StringValue ("2ms"));

// we will ask the PointToPointHelper to do the work involved in creating, 
// configuring and installing our devices for us.
  NetDeviceContainer devices;
  devices = pointToPoint.Install (nodes);

//  The Install method takes a NodeContainer as a parameter. When it is executed, 
// it will install an Internet Stack (TCP, UDP, IP, etc.) on each of the nodes in the node container.
  InternetStackHelper stack;
  stack.Install (nodes);

// it should begin allocating IP addresses from the network 10.1.1.0 
// using the mask 255.255.255.0 to define the allocatable bits.
  Ipv4AddressHelper address;
  address.SetBase ("10.1.1.0", "255.255.255.0");
// performs the actual address assignment
  Ipv4InterfaceContainer interfaces = address.Assign (devices);

  UdpEchoServerHelper echoServer (9);

  ApplicationContainer serverApps = echoServer.Install (nodes.Get (1));
  // Applications require a time to “start” generating traffic and may take an optional time to “stop”. 
  serverApps.Start (Seconds (1.0));
  serverApps.Stop (Seconds (10.0));

  UdpEchoClientHelper echoClient (interfaces.GetAddress (1), 9);
  echoClient.SetAttribute ("MaxPackets", UintegerValue (1));
  echoClient.SetAttribute ("Interval", TimeValue (Seconds (1.0)));
  echoClient.SetAttribute ("PacketSize", UintegerValue (1024));

  ApplicationContainer clientApps = echoClient.Install (nodes.Get (0));
  clientApps.Start (Seconds (2.0));
  clientApps.Stop (Seconds (10.0));

  Simulator::Run ();
  Simulator::Destroy ();
  return 0;
}
