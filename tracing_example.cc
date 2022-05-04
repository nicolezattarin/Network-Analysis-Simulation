#include "ns3/object.h"
#include "ns3/uinteger.h"
#include "ns3/traced-value.h"
#include "ns3/trace-source-accessor.h"

#include <iostream>

using namespace ns3;

// Since the tracing system is integrated with Attributes, and Attributes work with Objects,
// there must be an ns-3 Object for the trace source to live in

// a trace source is, in essence, a variable that holds a list of callbacks. 
// A trace sink is a function used as the target of a callback.
class MyObject : public Object
{
public:
  static TypeId GetTypeId (void)
  {
    static TypeId tid = TypeId ("MyObject")
      .SetParent<Object> ()
      .SetGroupName ("Tutorial")
      .AddConstructor<MyObject> ()
      // AddTraceSource provides the “hooks” used for connecting the trace source to the outside world through the Config system. 
      // args:
      // - name for this trace source, which makes it visible in the Config system. 
      // - second argument is a help string.
      // - arg of the third arg is the TracedValue which is being added to the class; (always a class data member)
      // - name of a typedef for the TracedValue type, as a string.
      .AddTraceSource ("MyInteger",
                       "An integer value to trace.",
                       MakeTraceSourceAccessor (&MyObject::m_myInt),
                       "ns3::TracedValueCallback::Int32");
    return tid;
  }

  MyObject () {}
  // provides the infrastructure that drives the callback process. 
  // Any time the underlying value is changed the TracedValue mechanism will provide both 
  // the old and the new value of that variable, in this case an int32_t value
  TracedValue<int32_t> m_myInt;
};
//callback function signature
void IntTrace (int32_t oldValue, int32_t newValue){
  std::cout << "Traced " << oldValue << " to " << newValue << std::endl;
}

int main (int argc, char *argv[])
{
  // connect the trace source to the callback function
  Ptr<MyObject> myObject = CreateObject<MyObject> ();
  myObject->TraceConnectWithoutContext ("MyInteger", MakeCallback (&IntTrace));

  myObject->m_myInt = 1234;
}
