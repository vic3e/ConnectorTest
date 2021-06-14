class JoinMessage():
    def __init__(self, IP, port):
        self.nodeID = None
        self.type = None # join, query, matcher
        self.IP = IP
        self.port = port
        self.registeredNodes = {}


    def setNodeID(self, nodeID):
        self.nodeID = nodeID


    def getNodeID(self):
        return self.nodeID


    def setIP(self, IP):
        self.IP = IP


    def setPort(self, port):
        self.port = port


    def getIP(self):
        return self.IP


    def getPort(self):
        return self.port


    def getType(self):
        return self.type


    def setType(self, type):
        self.type = type


    def setRegisteredNodes(self, nodes):
        self.registeredNodes = nodes


    def getRegisteredNodes(self):
        return self.registeredNodes


class Message(object):


    def __init__(self, senderNodeID, type):
        self.senderID = senderNodeID
        self.type = type


    def __init__(self, senderNodeID, type, channel=None, payload=None):
        self.senderID = senderNodeID
        self.type = type
        self.channel = channel
        self.payload = payload


    def setSenderID(self, id):
        self.senderID = id


    def setType(self, type):
        self.type = type


    def setPayload(self, payload):
        self.payload = payload


    def setChannel(self, channel):
        self.channel = channel


    def setArea(self, area):
        self.area = area


    def getSenderID(self):
        return self.senderID


    def getType(self):
        return self.type


    def getPayload(self):
        return self.payload


    def getChannel(self):
        return self.channel


    def getArea(self):
        return self.area
