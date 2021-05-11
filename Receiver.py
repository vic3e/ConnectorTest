import signalslot
from Connector import *

class MatcherExample(object):
    
    
    def __init__(self, id, ip, port, payload):
        self.id = id
        self.ip = ip
        self.port = port
        self.payload = payload
        # self.destination = destination


    def sender(self, destination_ip, destination_port):
        self.destination_ip = destination_ip
        self.destination_port = destination_port

        def sendernode(**kwargs):
            response = "\nThis is response: " + self.payload
            return

        signal_m = signalslot.Signal()
        
        signal_m.connect(sendernode)
        #emit/broadcast signal

        s_m = signal_m.emit()
        print('\nThis is signal from ', self.id, s_m)
        
        #where s1 == self.ip

        # FakeNetwork(s_m, self.port, destination_ip, destination_port, s_m)
       
        
        # print(self.ip, self.port, self.message, self.destination)
        # msg = "this is matcher" + self.message
        # print(msg)
