/* CODE FROM NS3 TUTORIALS */

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"

using namespace ns3;
/*************************************************************************************/
/*         (Echo client) o ---- o (Echo server)     PointToPoint channel             */
/*************************************************************************************/

// declares a logging component called log_example that allows to enable and disable 
// console message logging by reference to the name
NS_LOG_COMPONENT_DEFINE ("log_example");

int main (int argc, char *argv[])
{
  CommandLine cmd;
  cmd.Parse (argc, argv);
  // SETUP
  // set time resolution to nanoseconds
  Time::SetResolution (Time::NS);
  // set logging level for all components to LOG_DEBUG
  LogComponentEnable ("UdpEchoClientApplication", LOG_LEVEL_INFO);
  LogComponentEnable ("UdpEchoServerApplication", LOG_LEVEL_INFO);

  NS_LOG_INFO ("Creating Topology"); //INFO: log message with severity level of info
  // TOPOLOGY
  // create nodes o --- o
  NodeContainer nodes;
  nodes.Create (2);

  // create point-to-point (channel) link between nodes 0 and 1
  PointToPointHelper pointToPoint; //helpers are used to 
  pointToPoint.SetDeviceAttribute ("DataRate", StringValue ("5Mbps"));
  pointToPoint.SetChannelAttribute ("Delay", StringValue ("2ms"));
  pointToPoint.EnablePcapAll ("udp-echo-p2p");// enable pcap tracing on all devices

  //install on a net device
  // We create two PointToPointNetDevice: 
  // For each node in the nodes (there must be exactly two for a point-to-point link) a PointToPointNetDevice
  // is created and saved in the device container. 

  // We connect through a channel the two devices:
  // A  PointToPointChannel is created and the two PointToPointNetDevices are attached. 
  
  // attributes of helper are set in the device
  NetDeviceContainer devices;
  devices = pointToPoint.Install (nodes);

  // install protocol protocol stacks (i.e. an implementation of a computer networking protocol suite)
  InternetStackHelper stack;
  stack.Install (nodes);

  // assign IP addresses to the nodes
  // begin allocating IP addresses from the network 10.1.1.0 using the mask 255.255.255.0 to define the allocatable bits.
  Ipv4AddressHelper address;
  address.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer interfaces = address.Assign (devices);

  // CREATE APPLICATIONS
  // create a UdpEchoServerApplication on node 1
  // install a UdpEchoServerApplication on the node(1) of the NodeContainer . 
  // Install will return a container that holds pointers to all of the applications 
  // (one in this case since we passed a NodeContainer containing one node) created by the helper.
  UdpEchoServerHelper echoServer (9); // application which waits for input UDP packets and sends them back to the original sender.
                                      // PARAM: port the server will wait on for incoming packets

  ApplicationContainer serverApps = echoServer.Install (nodes.Get (1));
  // Applications require a time to “start” generating traffic and may take an optional time to “stop”.
  serverApps.Start (Seconds (1.0));
  serverApps.Stop (Seconds (10.0));

  UdpEchoClientHelper echoClient (interfaces.GetAddress (1), 9); //sends a UDP packet and waits for an echo of this packet.
                                                                // p	The IP address of the remote udp echo server
                                                                // port	The port number of the remote udp echo server
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
