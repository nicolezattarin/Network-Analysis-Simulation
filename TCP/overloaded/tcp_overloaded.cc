#include <fstream>
#include <iostream>
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"

using namespace ns3;
using namespace std;

NS_LOG_COMPONENT_DEFINE ("TCPlinkScriptExample");

// ===========================================================================
//
// TCP on overloaded link
//
// ===========================================================================
//
class MyApp : public Application
{
public:
  MyApp ();
  virtual ~MyApp ();
  static TypeId GetTypeId (void);
  void Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate);

private:
  virtual void StartApplication (void);
  virtual void StopApplication (void);

  void ScheduleTx (void);
  void SendPacket (void);

  Ptr<Socket>     m_socket;
  Address         m_peer;
  uint32_t        m_packetSize;
  uint32_t        m_nPackets;
  DataRate        m_dataRate;
  EventId         m_sendEvent;
  bool            m_running;
  uint32_t        m_packetsSent;
};

MyApp::MyApp (): m_socket (0),
                m_peer (),
                m_packetSize (0),
                m_nPackets (0),
                m_dataRate (0),
                m_sendEvent (),
                m_running (false),
                m_packetsSent (0)
{}

MyApp::~MyApp (){m_socket = 0;}

/* static */
TypeId MyApp::GetTypeId (void){
  static TypeId tid = TypeId ("MyApp")
                      .SetParent<Application> ()
                      .SetGroupName ("Tutorial")
                      .AddConstructor<MyApp> ();
  return tid;
}

void MyApp::Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate){
  m_socket = socket;
  m_peer = address;
  m_packetSize = packetSize;
  m_nPackets = nPackets;
  m_dataRate = dataRate;
}

void MyApp::StartApplication (void){
  m_running = true;
  m_packetsSent = 0;
  m_socket->Bind ();
  m_socket->Connect (m_peer);
  SendPacket ();
}

void MyApp::StopApplication (void){
  m_running = false;
  if (m_sendEvent.IsRunning ()){Simulator::Cancel (m_sendEvent);}
  if (m_socket){m_socket->Close ();}
}

void MyApp::SendPacket (void){
  Ptr<Packet> packet = Create<Packet> (m_packetSize);
  m_socket->Send (packet);

  if (++m_packetsSent < m_nPackets){ScheduleTx ();}
}

void MyApp::ScheduleTx (void){
  if (m_running){
      Time tNext (Seconds (m_packetSize * 8 / static_cast<double> (m_dataRate.GetBitRate ())));
      m_sendEvent = Simulator::Schedule (tNext, &MyApp::SendPacket, this);
    }
}

int main (int argc, char *argv[]){
  
  float DataRateR1 = 400; // in Kbps
  float DataRateR2 = 400; // in Kbps
  float DataRateR3 = 100; // in Kbps
  float DataRateR4 = 100; // in Kbps
  float DataRateC1 = 1000; // in Kbps
  float DataRateC2 = 10000; // in Kbps
  float DataRateC3 = 200; // in Kbps
  float delay = 1; // in milliseconds

  CommandLine cmd;
  cmd.AddValue ("DataRateR1", "DataRate R1 ", DataRateR1);
  cmd.AddValue ("DataRateR2", "DataRate R2", DataRateR2);
  cmd.AddValue ("DataRateR3", "DataRate R3", DataRateR3);
  cmd.AddValue ("DataRateR4", "DataRate R4", DataRateR4);
  cmd.AddValue ("DataRateC1", "DataRate C1", DataRateC1);
  cmd.AddValue ("DataRateC2", "DataRate C2", DataRateC2);
  cmd.AddValue ("DataRateC3", "DataRate C3", DataRateC3);
  cmd.Parse (argc, argv);
  
  // TOPOLOGY
  // Link 1
  NodeContainer nodes_L1;
  nodes_L1.Create (2); // nodes n0 and n1

  PointToPointHelper pointToPoint_L1;
  pointToPoint_L1.SetDeviceAttribute ("DataRate", StringValue (to_string(DataRateC1) + "Kbps"));
  pointToPoint_L1.SetChannelAttribute ("Delay", StringValue (to_string(delay)+"ms"));

  NetDeviceContainer devices_L1;
  devices_L1 = pointToPoint_L1.Install (nodes_L1);
  
  // Link 2
  NodeContainer nodes_L2;
  nodes_L2.Add(nodes_L1.Get(0));  // reference to n0
  nodes_L2.Create(1);
  
  PointToPointHelper pointToPoint_L2;
  pointToPoint_L2.SetDeviceAttribute ("DataRate", StringValue(to_string(DataRateC2) + "Kbps"));
  pointToPoint_L2.SetChannelAttribute ("Delay", StringValue (to_string(delay)+"ms"));

  NetDeviceContainer devices_L2;
  devices_L2 = pointToPoint_L2.Install (nodes_L2);

  // Link 3
  NodeContainer nodes_L3;
  nodes_L3.Add(nodes_L1.Get(0));   // reference to n0
  nodes_L3.Create(1);
  
  PointToPointHelper pointToPoint_L3;
  pointToPoint_L3.SetDeviceAttribute ("DataRate", StringValue (to_string(DataRateC3) + "Kbps"));
  pointToPoint_L3.SetChannelAttribute ("Delay", StringValue (to_string(delay)+"ms"));

  NetDeviceContainer devices_L3;
  devices_L3 = pointToPoint_L3.Install (nodes_L3);

  // Internet Stack
  InternetStackHelper stack; // declared only here
  stack.Install (nodes_L1);
  stack.Install (nodes_L2.Get(1));
  stack.Install (nodes_L3.Get(1));

  // Assign IP Addresses
  Ipv4AddressHelper address; // declared only here
  address.SetBase ("10.1.1.0", "255.255.255.252");
  Ipv4InterfaceContainer interfaces_L1 = address.Assign (devices_L1);
  address.SetBase ("10.1.2.0", "255.255.255.252");
  Ipv4InterfaceContainer interfaces_L2 = address.Assign (devices_L2);
  address.SetBase ("10.1.3.0", "255.255.255.252");
  Ipv4InterfaceContainer interfaces_L3 = address.Assign (devices_L3);

  // Setup Routing
  Ipv4GlobalRoutingHelper::PopulateRoutingTables ();
  
  // Applications  (Rate = App)
  // Rate 1: destination  n1
  // a packet sink receives and consumes traffic generated to an IP address and port.
  uint16_t sinkPort1 = 8080;
  Address sinkAddress1 (InetSocketAddress (interfaces_L1.GetAddress (1), sinkPort1)); //address of n1

  PacketSinkHelper packetSinkHelper1 ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), sinkPort1));
  ApplicationContainer sinkApps1 = packetSinkHelper1.Install (nodes_L1.Get (1)); //n1
  sinkApps1.Start (Seconds (0.));
  sinkApps1.Stop (Seconds (20.));  

  // origin node n2
  Ptr<Socket> ns3TcpSocket1 = Socket::CreateSocket (nodes_L2.Get (1), TcpSocketFactory::GetTypeId ());
  Ptr<MyApp> app1 = CreateObject<MyApp> ();
  app1->Setup (ns3TcpSocket1, sinkAddress1, 1040, 1000, DataRate ("400kbps"));
  nodes_L2.Get (1)->AddApplication (app1);
  app1->SetStartTime (Seconds (1.));
  app1->SetStopTime (Seconds (20.));
  
  // Rate 2: destination  n1
  uint16_t sinkPort2 = 8081;
  Address sinkAddress2 (InetSocketAddress (interfaces_L1.GetAddress (1), sinkPort2));
  PacketSinkHelper packetSinkHelper2 ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), sinkPort2));
  ApplicationContainer sinkApps2 = packetSinkHelper2.Install (nodes_L1.Get (1));
  sinkApps2.Start (Seconds (0.));
  sinkApps2.Stop (Seconds (20.));
  
  // Rate 2: origin n2
  Ptr<Socket> ns3TcpSocket2 = Socket::CreateSocket (nodes_L2.Get (1), TcpSocketFactory::GetTypeId ());
  Ptr<MyApp> app2 = CreateObject<MyApp> ();
  app2->Setup (ns3TcpSocket2, sinkAddress2, 1040, 1000, DataRate (to_string(DataRateR2) + "Kbps"));
  nodes_L2.Get (1)->AddApplication (app2);
  app2->SetStartTime (Seconds (1.));
  app2->SetStopTime (Seconds (20.));

  // Rate 3: destination  n1
  
  uint16_t sinkPort3 = 8082;
  Address sinkAddress3 (InetSocketAddress (interfaces_L1.GetAddress (1), sinkPort3));
  PacketSinkHelper packetSinkHelper3 ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), sinkPort3));
  ApplicationContainer sinkApps3 = packetSinkHelper3.Install (nodes_L1.Get (1));
  sinkApps3.Start (Seconds (0.));
  sinkApps3.Stop (Seconds (20.));

  // Rate 3: origin n3
  Ptr<Socket> ns3TcpSocket3 = Socket::CreateSocket (nodes_L3.Get (1), TcpSocketFactory::GetTypeId ());

  Ptr<MyApp> app3 = CreateObject<MyApp> ();
  app3->Setup (ns3TcpSocket3, sinkAddress3, 1040, 1000, DataRate (to_string(DataRateR3) + "Kbps"));
  nodes_L3.Get (1)->AddApplication (app3);
  app3->SetStartTime (Seconds (1.));
  app3->SetStopTime (Seconds (20.));

  // Rate 4: destination  n1
  uint16_t sinkPort4 = 8083;
  Address sinkAddress4 (InetSocketAddress (interfaces_L1.GetAddress (1), sinkPort4));
  PacketSinkHelper packetSinkHelper4 ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), sinkPort4));
  ApplicationContainer sinkApps4 = packetSinkHelper4.Install (nodes_L1.Get (1));
  sinkApps4.Start (Seconds (0.));
  sinkApps4.Stop (Seconds (20.));

  // Rate 4: origin n3
  Ptr<Socket> ns3TcpSocket4 = Socket::CreateSocket (nodes_L3.Get (1), TcpSocketFactory::GetTypeId ());

  Ptr<MyApp> app4 = CreateObject<MyApp> ();
  app4->Setup (ns3TcpSocket4, sinkAddress4, 1040, 1000, DataRate (to_string(DataRateR4) + "Kbps"));
  nodes_L3.Get (1)->AddApplication (app4);
  app4->SetStartTime (Seconds (1.));
  app4->SetStopTime (Seconds (20.));

  // pcap recording on "receiving" net devices
  pointToPoint_L1.EnablePcap ("tcp-link", nodes_L1.Get (1)->GetId (), 0);
  pointToPoint_L2.EnablePcap ("tcp-link", nodes_L2.Get (0)->GetId (), 0);
  pointToPoint_L3.EnablePcap ("tcp-link", nodes_L3.Get (0)->GetId (), 0);

  Simulator::Stop (Seconds (20));
  Simulator::Run ();
  Simulator::Destroy ();

  return 0;
}

