#include "ns3/core-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/network-module.h"
#include "ns3/applications-module.h"
#include "ns3/mobility-module.h"
#include "ns3/csma-module.h"
#include "ns3/internet-module.h"
#include "ns3/yans-wifi-helper.h"
#include "ns3/ssid.h"

// Default Network Topology: number of wifi and lan can be changed
//
//   Wifi 10.1.3.0
//                 AP
//  *    *    *    *
//  |    |    |    |    10.1.1.0
// n5   n6   n7   n0 -------------- n1   n2   n3   n4
//                   point-to-point  |    |    |    |
//                                   ================
//                                     LAN 10.1.2.0

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("wireless_net");
void CourseChange (std::string context, Ptr<const MobilityModel> model){
  Vector position = model->GetPosition ();
  NS_LOG_UNCOND (context <<" x = " << position.x << ", y = " << position.y);
}


int main (int argc, char *argv[])
{
    // SETUP
    bool verbose = true;
    uint32_t nCsma = 3; // number of Carrier Sense Multiple Access
    uint32_t nWifi = 3; // number of wifi devices
    bool tracing = false;


    CommandLine cmd;
    cmd.AddValue ("nCsma", "Number of \"extra\" CSMA nodes/devices", nCsma);
    cmd.AddValue ("verbose", "Tell echo applications to log if true", verbose);
    cmd.AddValue ("nWifi", "Number of wifi devices", nWifi);
    cmd.AddValue ("tracing", "Enable pcap tracing", tracing);

    cmd.Parse (argc,argv);

    if (verbose){
    LogComponentEnable ("UdpEchoClientApplication", LOG_LEVEL_INFO);
    LogComponentEnable ("UdpEchoServerApplication", LOG_LEVEL_INFO);}

    if (nWifi > 18){
        std::cout << "nWifi should be 18 or less; otherwise grid layout exceeds the bounding box" << std::endl;
        return 1;}
    if (nCsma == 0){
        NS_LOG_WARN ("No CSMA nodes specified, automatically creating one");
        nCsma = 1;}
    if (nWifi == 0){
        NS_LOG_WARN ("No wifi nodes specified, automatically creating one");
        nWifi = 1;}
    
    // nodes
    NS_LOG_INFO ("CREATING TOPOLOGY");
    NodeContainer p2pNodes;
    p2pNodes.Create (2);

    NodeContainer csmaNodes;
    csmaNodes.Add (p2pNodes.Get (1)); 
    csmaNodes.Create (nCsma);

    NodeContainer wifiStaNodes;
    wifiStaNodes.Create (nWifi);
    NodeContainer wifiApNode = p2pNodes.Get (0);

    //channel p2p
    PointToPointHelper pointToPoint;
    pointToPoint.SetDeviceAttribute ("DataRate", StringValue ("5Mbps"));
    pointToPoint.SetChannelAttribute ("Delay", StringValue ("2ms"));

    // devices p2p
    NetDeviceContainer p2pDevices;
    p2pDevices = pointToPoint.Install (p2pNodes);

    //channel csma
    CsmaHelper csma;
    csma.SetChannelAttribute ("DataRate", StringValue ("100Mbps"));
    csma.SetChannelAttribute ("Delay", TimeValue (NanoSeconds (6560)));

    NetDeviceContainer csmaDevices;
    csmaDevices = csma.Install (csmaNodes);

    //channel wifi: a Wi-Fi model needs four helper objects (
    // YansWifiChannelHelper, YansWifiPhyHelper, WifiMacHelper, WifiHelper) and an service set identifier object 

    //channel
    YansWifiChannelHelper channel = YansWifiChannelHelper::Default ();
    //phy
    YansWifiPhyHelper phy = YansWifiPhyHelper::Default ();
    // we create a channel object and associate it to our PHY layer object manager
    phy.SetChannel (channel.Create ());
    // mac
    WifiMacHelper mac;
    // creates an 802.11 service set identifier (SSID) to set the “Ssid” Attribute of MAC .
    Ssid ssid = Ssid ("ns-3-ssid");
    // WifiHelper: standard WIFI 6 configure a compatible rate control algorithm (IdealWifiManager).
    WifiHelper wifi;
    // device
    NetDeviceContainer staDevices;
    // set type:
    //Parameters
    // type:	the type of ns3::WifiMac to create.
    // args:	A sequence of name-value pairs of the attributes to set.
    mac.SetType ("ns3::StaWifiMac", "Ssid", SsidValue (ssid), "ActiveProbing", BooleanValue (false));
    staDevices = wifi.Install (phy, mac, wifiStaNodes); // inrge whifi helper

    // configure the AP (access point) node
    mac.SetType ("ns3::ApWifiMac", "Ssid", SsidValue (ssid));
    NetDeviceContainer apDevices;
    apDevices = wifi.Install (phy, mac, wifiApNode);


    // Mobility
    // STA nodes mobile in a box, AP node stationary
    MobilityHelper mobility;
    mobility.SetPositionAllocator ("ns3::GridPositionAllocator",
            "MinX", DoubleValue (0.0),
            "MinY", DoubleValue (0.0),
            "DeltaX", DoubleValue (5.0),
            "DeltaY", DoubleValue (10.0),
            "GridWidth", UintegerValue (3),
            "LayoutType", StringValue ("RowFirst"));
    // how to move
    mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel",
            "Bounds", RectangleValue (Rectangle (-50, 50, -50, 50)));

    mobility.Install (wifiStaNodes);
    mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
    mobility.Install (wifiApNode);

    // Internet stack
    InternetStackHelper stack;
    stack.Install (csmaNodes);
    stack.Install (wifiApNode);
    stack.Install (wifiStaNodes);

    // assign IP address
    Ipv4AddressHelper address;
    address.SetBase ("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer p2pInterfaces;
    p2pInterfaces = address.Assign (p2pDevices);

    address.SetBase ("10.1.2.0", "255.255.255.0");
    Ipv4InterfaceContainer csmaInterfaces;
    csmaInterfaces = address.Assign (csmaDevices);

    address.SetBase ("10.1.3.0", "255.255.255.0");
    address.Assign (staDevices);
    address.Assign (apDevices);

    // Applications
    UdpEchoServerHelper echoServer (9);

    ApplicationContainer serverApps = echoServer.Install (csmaNodes.Get (nCsma));
    serverApps.Start (Seconds (1.0));
    serverApps.Stop (Seconds (10.0));

    UdpEchoClientHelper echoClient (csmaInterfaces.GetAddress (nCsma), 9);
    echoClient.SetAttribute ("MaxPackets", UintegerValue (1));
    echoClient.SetAttribute ("Interval", TimeValue (Seconds (1.0)));
    echoClient.SetAttribute ("PacketSize", UintegerValue (1024));
    
    ApplicationContainer clientApps = echoClient.Install (wifiStaNodes.Get (nWifi - 1));
    clientApps.Start (Seconds (2.0));
    clientApps.Stop (Seconds (10.0));

    Ipv4GlobalRoutingHelper::PopulateRoutingTables ();

    // the simulation we just created will never “naturally” stop, force it
    Simulator::Stop (Seconds (10.0));

    if (tracing == true){
      pointToPoint.EnablePcapAll ("wifi");
      phy.EnablePcap ("wifi", apDevices.Get (0));
      csma.EnablePcap ("wifi", csmaDevices.Get (0), true); }

    std::ostringstream oss;
    oss <<"/NodeList/" << wifiStaNodes.Get (nWifi - 1)->GetId () << "/$ns3::MobilityModel/CourseChange";
    Config::Connect (oss.str (), MakeCallback (&CourseChange));

    // run the simulation
    Simulator::Run ();
    Simulator::Destroy ();
    return 0;
}


