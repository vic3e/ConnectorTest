from abc import ABC, abstractmethod
import signalslot
from Receiver import *

nodedictionary = {} # Dictionary to store nodes into slots -> {"IPORT": IP n PORT, "Slot"}

destinationdict = {} #


class NetworkInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def receive(self):
        pass


class RealNetwork(NetworkInterface):
    
    def connect(self, sender_ip, sender_port, destination_ip, destination_port):
        pass

    def send(self):
        # connect to something for real
        
        return

    def receive(self):
        # transfer a bunch of data
        return


class FakeSocket(object):

    def __init__(self, fakeip, fakeport, payload):
        # SenderIP (signal), SenderPort
        self.fakeip = fakeip
        self.fakeport = fakeport   
        self.payload = payload



    def connect(self, destination_ip, destination_port):
        self.destination_ip = destination_ip
        self.destination_port = destination_port


        nodeid = (self.fakeip, self.fakeport)
        destination = (destination_ip, destination_port)

        # Add signal/request to dictionary
        nodedictionary = {"nodesignal":[], "payload":[], "destination":[]}
        nodedictionary["nodesignal"].append(self.fakeip)
        nodedictionary["payload"].append(self.payload)
        nodedictionary["destination"].append(destination_ip)

        
        print(nodedictionary["nodesignal"])

        # Connect function to signal
        # self.n_conf.connect(yourmodule_conf)
        # lookup destination dictionary
        # pass


    def bind(self):
        print('\n*** This is binding process ***')
        
        # print 
        m = self.nodedictionary["nodesignal"]
        if m == "node1":

            #note: add argument
            m1 = MatcherExample()  #lookup node id
            m1.sender(self.destination_ip, self.destination_port)
        
        #     # if self.nodedictionary["destination"] == "matcher one":
        #     print("Send payload to matcher one")


    def listen(self):
        # print(m_conf)
        pass
        

class FakeNetwork(NetworkInterface):

    def __init__(self,sender_ip, sender_port, destination_ip, destination_port, payload):
        # sender_ip = 127.0.0.1;
        self.sender_ip = sender_ip
        self.sender_port = sender_port
        self.destination_ip = destination_ip
        self.destination_port = destination_port
        self.payload = payload

        self.socket = FakeSocket(sender_ip, sender_port, payload)
        self.socket.connect(destination_ip, destination_port)
        
        # sender_ip()

    def connect(self):

        self.socket.connect(self.sender_ip, self.sender_port)



    def bind(self):
        self.socket.bind(self)
        

    def listen(self):
        self.socket.listen()


    def send(self, Request):
        
        return

    def receive(self):

        return
