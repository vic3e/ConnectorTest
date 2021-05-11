
from Connector import *
import signalslot

class NodeExample(object):
    
    def __init__(self, id, ip, port, payload):
        self.id = id
        self.ip = ip
        self.port = port
        self.payload = payload


    def pubsend(self, destination_ip, destination_port):
        self.destination_ip = destination_ip
        self.destination_port = destination_port

        def sendernode(**kwargs):
            msg = "\nThis is payload from node: " + self.payload
            return self.payload

        signal = signalslot.Signal()
        
        signal.connect(sendernode)
        #emit/broadcast signal

        s1 = signal.emit()
        print('\nThis is signal from ', self.id, signal)
        
        #where s1 == self.ip

        FakeNetwork(self.id, self.port, destination_ip, destination_port, self.payload)
        # print(ip, port, s1, destination_port, message)     


        # signal1.emit(data=msg)

        # request = (self.ip, self.port, self.message, destination_ip, destination_port)
        # print('\n', request)

        # publish message
        # pubrequest = FakeNetwork(self.ip, self.port, destination_ip, destination_port, self.message)


    def receive(self, receiver_ip, receiver_port, payload):
        pass