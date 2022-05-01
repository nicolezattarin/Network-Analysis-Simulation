
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/csma-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/ipv4-global-routing-helper.h"

// Default Network Topology
//
//       10.1.1.0
// n0 -------------- n1   n2   n3   n4
//    point-to-point  |    |    |    |
//                    ================
//                      LAN 10.1.2.0


using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("bus-example");

int 
main (int argc, char *argv[])
{
  // SETUP
  bool verbose = true;
  uint32_t nCsma = 3; // number of Carrier Sense Multiple Access

  CommandLine cmd;
  cmd.AddValue ("nCsma", "Number of \"extra\" CSMA nodes/devices", nCsma);
  cmd.AddValue ("verbose", "Tell echo applications to log if true", verbose);

  cmd.Parse (argc,argv);

  if (verbose){
      LogComponentEnable ("UdpEchoClientApplication", LOG_LEVEL_INFO);
      LogComponentEnable ("UdpEchoServerApplication", LOG_LEVEL_INFO);}
      
  if (nCsma == 0){
      NS_LOG_WARN ("No CSMA nodes specified, automatically creating one");
      nCsma = 1;}

  // nodes
  NS_LOG_INFO ("CREATING TOPOLOGY");
  NodeContainer p2pNodes;
  p2pNodes.Create (2);

  NodeContainer csmaNodes;
  csmaNodes.Add (p2pNodes.Get (1)); // get first node from p2p node container, 
                                    // add it to the container of nodes that will get CSMA devices. 
                                    // The node ends up with a p2p device and a CSMA device.
  csmaNodes.Create (nCsma);

  PointToPointHelper pointToPoint;
  pointToPoint.SetDeviceAttribute ("DataRate", StringValue ("5Mbps"));
  pointToPoint.SetChannelAttribute ("Delay", StringValue ("2ms"));

  NetDeviceContainer p2pDevices;
  p2pDevices = pointToPoint.Install (p2pNodes);

  CsmaHelper csma;
  csma.SetChannelAttribute ("DataRate", StringValue ("100Mbps"));
  csma.SetChannelAttribute ("Delay", TimeValue (NanoSeconds (6560)));

  NetDeviceContainer csmaDevices;
  csmaDevices = csma.Install (csmaNodes);

  NS_LOG_INFO ("CONFIGURING STACK AND IPv4");
  InternetStackHelper stack;
  // we took one of the nodes from the p2pNodes container and added it to the csmaNodes container. 
  // we only need to install the stacks on the remaining p2pNodes node and the csmaNodes node.
  stack.Install (p2pNodes.Get (0));
  stack.Install (csmaNodes);

  Ipv4AddressHelper address;

  address.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer p2pInterfaces;
  p2pInterfaces = address.Assign (p2pDevices);

  address.SetBase ("10.1.2.0", "255.255.255.0");
  Ipv4InterfaceContainer csmaInterfaces;
  csmaInterfaces = address.Assign (csmaDevices);

  NS_LOG_INFO ("CONFIGURING ROUTING");
  UdpEchoServerHelper echoServer (9);

  ApplicationContainer serverApps = echoServer.Install (csmaNodes.Get (nCsma));
  serverApps.Start (Seconds (1.0));
  serverApps.Stop (Seconds (10.0));

  UdpEchoClientHelper echoClient (csmaInterfaces.GetAddress (nCsma), 9);
  echoClient.SetAttribute ("MaxPackets", UintegerValue (1));
  echoClient.SetAttribute ("Interval", TimeValue (Seconds (1.0)));
  echoClient.SetAttribute ("PacketSize", UintegerValue (1024));

  ApplicationContainer clientApps = echoClient.Install (p2pNodes.Get (0));
  clientApps.Start (Seconds (2.0));
  clientApps.Stop (Seconds (10.0));

  // enable routing
  Ipv4GlobalRoutingHelper::PopulateRoutingTables ();

  pointToPoint.EnablePcapAll ("bus-p2p-csma");
  //get device from csma device container
  csma.EnablePcap ("bus-p2p-csma", csmaDevices.Get (1), true); // CsmaHelper 
  // final parameter tells the CSMA helper whether or not to arrange to capture packets in promiscuous mode.

  pointToPoint.EnablePcap ("bus-p2p-csma", p2pNodes.Get (0)->GetId (), 0);
  csma.EnablePcap ("bus-p2p-csma", csmaNodes.Get (nCsma)->GetId (), 0, false);
  csma.EnablePcap ("bus-p2p-csma", csmaNodes.Get (nCsma-1)->GetId (), 0, false);


  Simulator::Run ();
  Simulator::Destroy ();
  return 0;
}
