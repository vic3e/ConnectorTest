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
