from Sender import *
from Receiver import *
import signalslot

# 1 - Generate Node 1 data
id = "node1"
ip = "n.o.d.e.1"
port = '80'
message = "payload one"
destination_ip = "matcher one"
destination_port = "80"


# Generate Matcher 1 data
id1 = "node2"
ip1 = "n.o.d.e.2"
port1 = '80'
message1 = "request received"
destination1 = "matcher two"


n1 = NodeExample(id, ip, port, message)
n1.pubsend(destination_ip, destination_port)

n2 = MatcherExample(id1, ip1, port1, message1)
n2.sender(destination1, destination_port)


# #create destination signal
# destinationsignal = signalslot.Signal()


# def destination(**kwargs):
#     n2 = MatcherExample(id, ip, port, message)
#     # n2.send(destination_ip, destination_port)
#     return n1
    
     #print(n1)
# # Node1 ---> {connector} ---> Matcher1
# def sendernode(**kwargs):
#     n1 = NodeExample(id, ip, port, message)
#     n1.send(destination_ip, destination_port)
#     # return n1
#     #print(n1)

# # Connect function to signal
# signal1.connect(sendernode)

# #emit/broadcast signal
# # s1 = {}
# s1 = signal1.emit()

# print(s1)

# # x2 = s1.is_connected(sendernode)
# # print(x2)


# def receivernode(**kwargs):
#     n2 = NodeExample(id, ip, port, message)
#     n2.send(destination_ip, destination_port) 




#disconnect
# print(signal1)
# n1.is_connected(sendernode)


# Connect Node 1 to matcher 1

#subscribe to specific destination

# print(n1)

# m1 = NodeExample(id, ip, port, message, destination)
# m1.main(destination)