from Connector import NetworkInterface
from Message import JoinMessage

class VASTInterface(object):
    def __init__(self):
        self.registeredNodes = {}

    def join(self, IP, port, ID):
        self.registerNode(IP, port, ID)

    def registerNode(self, IP, port, nodeID):
        self.registeredNodes[nodeID] = (IP, port)
        #print(self.registeredNodes)


    def getIPPort(self, nodeID):
        #print(self.registeredNodes)
        result = self.registeredNodes[nodeID]
        return result