#include <fstream>
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"

using namespace ns3;
using namespace std;
NS_LOG_COMPONENT_DEFINE ("tcp_2nodes");

// ===========================================================================
//
//         node 0                 node 1
//   +----------------+    +----------------+
//   |    ns-3 TCP    |    |    ns-3 TCP    |
//   +----------------+    +----------------+
//   |    10.1.1.1    |    |    10.1.1.2    |
//   +----------------+    +----------------+
//   | point-to-point |    | point-to-point |
//   +----------------+    +----------------+
//           |                     |
//           +---------------------+
//                5 Mbps, 2 ms
//===============================================
//
class MyApp : public Application {
public:
  MyApp ();
  virtual ~MyApp();
  void Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate);

private:
  virtual void StartApplication (void);
  virtual void StopApplication (void);

  void ScheduleTx (void);
  void SendPacket (void);

  Ptr<Socket>     m_socket; //ip and port
  Address         m_peer;  
  uint32_t        m_packetSize;
  uint32_t        m_nPackets;
  DataRate        m_dataRate;
  EventId         m_sendEvent;
  bool            m_running;
  uint32_t        m_packetsSent;
};

// constructor
MyApp::MyApp ()
  : m_socket (0), 
    m_peer (), 
    m_packetSize (0), 
    m_nPackets (0), 
    m_dataRate (0), 
    m_sendEvent (), 
    m_running (false), 
    m_packetsSent (0)
{
}

// destructor
MyApp::~MyApp(){m_socket = 0;}

// the Ptr<Socket> socket which we needed to provide to the application during configuration time. 
// we are going to create the Socket as a TcpSocket and hook its “CongestionWindow” trace source before passing it to the Setup method.
void MyApp::Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate){
  m_socket = socket;
  m_peer = address;
  m_packetSize = packetSize;
  m_nPackets = nPackets;
  m_dataRate = dataRate;
}

// verridden implementation Application::StartApplication that will be automatically 
// called by the simulator to start our Application running at the appropriate time.
void MyApp::StartApplication (void){
  m_running = true;
  m_packetsSent = 0;
  m_socket->Bind ();
  m_socket->Connect (m_peer); // After the Connect, the Application then starts creating 
                              // simulation events by calling SendPacket.
  SendPacket ();
}

void MyApp::StopApplication (void){
  m_running = false;
  if (m_sendEvent.IsRunning ()){Simulator::Cancel (m_sendEvent);}
  if (m_socket){m_socket->Close ();}
}

// SendPacket is called by the simulator to send a packet.
void MyApp::SendPacket (void){
  Ptr<Packet> packet = Create<Packet> (m_packetSize); //create a packet of size m_packetSize
  m_socket->Send (packet); //send the packet to the socket
  if (++m_packetsSent < m_nPackets){ ScheduleTx ();} //schedule the next packet
}

// schedule the next packet transmission
void MyApp::ScheduleTx (void){
  if (m_running){
    // the data rate of an Application has nothing to do with the data rate of an underlying Channel. 
    // This is the rate at which the Application produces bits. 
      Time tNext (Seconds (m_packetSize * 8 / static_cast<double> (m_dataRate.GetBitRate ())));
      m_sendEvent = Simulator::Schedule (tNext, &MyApp::SendPacket, this);}
}

// Trace Sinks
static void CwndChange (Ptr<OutputStreamWrapper> stream, uint32_t oldCwnd, uint32_t newCwnd){
  NS_LOG_UNCOND (Simulator::Now ().GetSeconds () << "\t" << newCwnd); //output on terminal
  *stream->GetStream () << Simulator::Now ().GetSeconds () << "\t" << oldCwnd << "\t" << newCwnd << std::endl; //out to filestream
}

static void RxDrop (Ptr<OutputStreamWrapper> stream, Ptr<const Packet> p){
  NS_LOG_UNCOND (Simulator::Now ().GetSeconds ());
  *stream->GetStream () << Simulator::Now ().GetSeconds () << endl;
}


int main (int argc, char *argv[])
{
  CommandLine cmd;
  cmd.Parse (argc, argv);
  
  NodeContainer nodes;
  nodes.Create (2);

  PointToPointHelper pointToPoint;
  pointToPoint.SetDeviceAttribute ("DataRate", StringValue ("Mbps"));
  pointToPoint.SetChannelAttribute ("Delay", StringValue ("2ms"));

  NetDeviceContainer devices;
  devices = pointToPoint.Install (nodes);

  // RateErrorModel allows us to introduce errors into a Channel at a given rate.
  Ptr<RateErrorModel> em = CreateObject<RateErrorModel> ();
  em->SetAttribute ("ErrorRate", DoubleValue (0.00001));
  devices.Get (1)->SetAttribute ("ReceiveErrorModel", PointerValue (em));

  InternetStackHelper stack;
  stack.Install (nodes);

  Ipv4AddressHelper address;
  address.SetBase ("10.1.1.0", "255.255.255.252");
  Ipv4InterfaceContainer interfaces = address.Assign (devices);

  // Since we are using TCP, we need something on the destination Node to receive TCP connections 
  // and data. The PacketSink Application is commonly used in ns-3 for that purpose.
  uint16_t sinkPort = 8080;
  Address sinkAddress (InetSocketAddress (interfaces.GetAddress (1), sinkPort));
  // instantiates a PacketSinkHelper and tells it to create sockets using the class ns3::TcpSocketFactory
  // param tells the Application which address and port it should Bind to.
  PacketSinkHelper packetSinkHelper ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), sinkPort));
  ApplicationContainer sinkApps = packetSinkHelper.Install (nodes.Get (1));
  sinkApps.Start (Seconds (0.));
  sinkApps.Stop (Seconds (20.));
  // create the socket and connect the trace source.
  Ptr<Socket> ns3TcpSocket = Socket::CreateSocket (nodes.Get (0), TcpSocketFactory::GetTypeId ());
  
  AsciiTraceHelper asciiTraceHelper;
  Ptr<OutputStreamWrapper> streamCWindow = asciiTraceHelper.CreateFileStream ("streamCongestionWindow.txt");
  ns3TcpSocket->TraceConnectWithoutContext ("CongestionWindow", MakeBoundCallback (&CwndChange, streamCWindow));

  Ptr<MyApp> app = CreateObject<MyApp> ();
  app->Setup (ns3TcpSocket, sinkAddress, 1040, 1000, DataRate ("1Mbps"));
  nodes.Get (0)->AddApplication (app);

  // the simulator automatically makes calls into our Applications to tell them when to start and stop. 
  // In the case of MyApp, it inherits from class Application and overrides StartApplication, and StopApplication.
  app->SetStartTime (Seconds (1.));
  app->SetStopTime (Seconds (20.));

  Ptr<OutputStreamWrapper> DropStream = asciiTraceHelper.CreateFileStream ("DropStream.txt");
  devices.Get (1)->TraceConnectWithoutContext ("DropStream", MakeBoundCallback (&RxDrop, DropStream));

  Simulator::Stop (Seconds (20));
  Simulator::Run ();
  Simulator::Destroy ();

  return 0;
}

