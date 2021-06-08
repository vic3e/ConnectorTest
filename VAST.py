class VASTInterface(object):
    def __init__(self):
        self.registeredNodes = {}


    def join(self, nodeID, IP, port):
        self.registeredNodes[nodeID] = (IP, port)


    def getIPPort(self, nodeID):
        result = self.registeredNodes[nodeID]
        return result