from VAST import VASTInterface
from collections import defaultdict
from Message import Message, JoinMessage
import logging
from Connector import NetworkInterface

class Gateway():
    def __init__(self, interface):
        self.interface = interface
        self.ID = 0
        self.registeredNodes = {}
        self.matchers = []


    def initialiseNetworkInterface(self):
        self.interface.bind()

    def processSingleMessage(self):

        #logging.info("Gateway::processSingleMessage => Number of received messages <%d>" % self.interface.getNumberOfMessages())
        if (self.interface.getNumberOfMessages()):
            message = self.interface.getMessage()
            type = message.getType()
            #logging.info("Gateway::processSingleMessage => Received message of type <%s>" % type)
            if (type == 'join'):
                IP = message.getIP()
                port = message.getPort()
                nodeID = self.generateID(IP, port)
                self.registerNode(IP, port, nodeID)
                message.setRegisteredNodes(self.registeredNodes)
                for ID in self.registeredNodes:
                    (nodeIP, nodePort) = self.registeredNodes[ID]
                    message.setIP(nodeIP)
                    message.setPort(nodePort)
                    message.setNodeID(ID)
                    self.interface.connect(nodeIP, nodePort)
                    self.interface.send(message)
            elif (type == 'matcher'):
                nodeID = message.getNodeID()
                self.registerMatcher(nodeID)
            elif (type == 'query'):
                nodeID = message.getNodeID()
                (IP, port) = self.queryNodeID(nodeID)
                message.setIP(IP)
                message.setPort(port)
                self.interface.connect(IP, port)
                self.interface.send(message)


    def generateID(self, IP, port):
        nodeID = self.ID
        self.ID += 1
        return nodeID


    def registerNode(self, IP, port, nodeID):
        self.registeredNodes[nodeID] = (IP, port)


    def registerMatcher(self, nodeID):
        self.matchers.append(nodeID)


    def queryNodeID(self, nodeID):
        (IP, port) = self.registeredNodes[nodeID]
        return (IP, port)


class SPSNode(object):


    def __init__(self, VASTNode, matcherID):
        self.VASTNode = VASTNode
        self.matcherID = matcherID


    def publishToChannel(self, channel, message):
        msg = Message(self.VASTNode.getNodeID(), 'pub', channel, message)
        self.VASTNode.send(self.matcherID, msg)


    def publishToArea(self, area, message):
        msg = Message(self.VASTNode.getNodeID(), 'spatialpub')
        msg.setArea(area)
        msg.setPayload(message)
        self.VASTNode.send(self.matcherID, msg)


    def subscribeToChannel(self, channel):
        msg = Message(self.VASTNode.getNodeID(), 'sub', channel)
        self.VASTNode.send(self.matcherID, msg)


    def unsubscribeFromChannel(self, channel):
        msg = Message(self.VASTNode.getNodeID(), 'unsub', channel)
        self.VASTNode.send(self.matcherID, msg)


    def subscribeToArea(self, area):
        msg = Message(self.VASTNode.getNodeID(), 'spatialsub')
        msg.setArea(area)
        self.VASTNode.send(self.matcherID, msg)


    def unsubscribeFromArea(self, area):
        msg = Message(self.VASTNode.getNodeID(), 'spatialunsub')
        msg.setArea(area)
        self.VASTNode.send(self.matcherID, msg)


class VASTNode(object):


    def __init__(self, networkInterface, VASTInterface):
        self.nodeID = None
        self.networkInterface = networkInterface
        self.VAST = VASTInterface


    def initialiseNetworkInterface(self):
        self.networkInterface.bind()


    def registerID(self, gatewayIP, gatewayPort):
        IP = self.networkInterface.getIP()
        port = self.networkInterface.getPort()
        message = JoinMessage(IP, port)
        message.setType('join')
        self.networkInterface.connect(gatewayIP, gatewayPort)
        self.networkInterface.send(message)


    def connect(self, IP, port):
        self.networkInterface.connect(destinationIP=IP, destinationPort=port)


    def send(self, destinationNodeID, message):
        #logging.info("VASTNode::send => Node [%s] is sending message with content '%s' to node [%s]" % (self.nodeID, message.getPayload(), destinationNodeID))
        (IP, port) = self.VAST.getIPPort(destinationNodeID)
        #message.setSenderID(self.getNodeID())
        self.networkInterface.connect(IP, port)
        self.networkInterface.send(message=message)


    def processSingleMessage(self):
        #logging.info("Gateway::processSingleMessage => Number of received messages <%d>" % self.networkInterface.getNumberOfMessages())

        if (self.networkInterface.getNumberOfMessages()):
            message = self.networkInterface.getMessage()
            type = message.getType()
            #logging.info("VASTNode::processSingleMessage => Received message of type <%s>" % type)
            if (type == 'join'):
                self.nodeID = message.getNodeID()
                IP = self.networkInterface.getIP()
                port = self.networkInterface.getPort()
                self.VAST.join(IP, port, self.nodeID)
                registeredNodes = message.getRegisteredNodes()
                for nodeID in registeredNodes:
                    (nodeIP, nodePort) = registeredNodes[nodeID]
                    self.VAST.join(nodeIP, nodePort, nodeID)
                logging.info("VASTNode::handleMessage => MatcherNode::handleMessage => Received nodeID <%s> from gateway" % self.nodeID)
            else:
                payload = message.getPayload()
                senderID = message.getSenderID()
                channel = message.getChannel()
                logging.info("VASTNode::handleMessage => Node [%s] has received message type <%s> for channel <%s> from node [%s] with content '%s'" % (self.nodeID, type, channel, senderID, payload))
                # logging.info("VASTNode::processSingleMessage => Node [%s] has received message <%s> from node [%s] with content '%s'" % (self.nodeID, type, senderID, payload))
                # print("Node [%s] has <%d> messages left in queue" % (self.nodeID, self.networkInterface.getNumberOfMessages()) )


    def processMessages(self):
        while (self.networkInterface.getNumberOfMessages()):
            message = self.networkInterface.getMessage()
            payload = message.getPayload()
            senderID = message.getSenderID()
            type = message.getType()
            channel = message.getChannel()
            logging.info("VASTNode::handleMessage => Node [%s] has received message type <%s> for channel <%s> from node [%s] with content '%s'" % (self.nodeID, type, channel, senderID, payload))
#           # print("Node [%s] has <%d> messages left in queue" % (self.nodeID, self.networkInterface.getNumberOfMessages()) )


    def receive(self, message, **kwargs):
        print('Node id {self.id} received: "{message.payload}" from Node id: {message.sender_id}')


    def getNodeID(self):
        return self.nodeID


class MatcherNode(VASTNode):


    def __init__(self, networkInterface, VASTInterface):
        self.nodeID = None
        self.networkInterface = networkInterface
        self.VAST = VASTInterface
        self.channelSubscriptions = defaultdict()
        self.spatialSubscriptions = defaultdict()


    def handleMessage(self, message):
        type = message.getType()
        #
        #logging.info("Matcher::handleMessage => Matcher handling message <%s> from node <%s>" % (type, senderID))
        if type == 'sub':
            senderID = message.getSenderID()
            channel = message.getChannel()
            logging.info("Matcher::handleMessage => Node <%s> subscribing to channel <%s>" % (senderID, channel))
            self.addChannelSubscription(senderID, channel)
        elif type == 'unsub':
            senderID = message.getSenderID()
            channel = message.getChannel()
            logging.info("Matcher::handleMessage => Node <%s> unsubscribing from channel <%s>" % (senderID, channel))
            self.removeChannelSubscription(senderID, channel)
        elif type == 'pub':
            senderID = message.getSenderID()
            channel = message.getChannel()
            payload = message.getPayload()
            logging.info("Matcher::handleMessage => Node <%s> publishing message '%s' to channel <%s>" % (senderID, payload, channel))
            self.publishChannel(senderID, channel, payload)
        elif type == 'deliverpub':
            payload = message.getPayload()
            senderID = message.getSenderID()
            type = message.getType()
            channel = message.getChannel()
            logging.info("Matcher::handleMessage => Node [%s] has received message type <%s> for channel <%s> from node [%s] with content '%s'" % (self.nodeID, type, channel, senderID, payload))
        elif type == 'spatialsub':
            senderID = message.getSenderID()
            area = message.getArea()
            logging.info("Matcher::handleMessage => Node <%s> subscribing to area <%d,%d,%d>" % (senderID, area.position[0], area.position[1],area.radius))
            self.addSpatialSubscription(senderID, area)
        elif type == 'spatialunsub':
            senderID = message.getSenderID()
            area = message.getArea()
            logging.info("Matcher::handleMessage => Node <%s> unsubscribing from area <%d,%d,%d>" % (senderID, area.position[0], area.position[1],area.radius))
            self.removeSpatialSubscription(senderID, area)
        elif type == 'spatialpub':
            senderID = message.getSenderID()
            area = message.getArea()
            payload = message.getPayload()
            logging.info("Matcher::handleMessage => MatcherNode::handleMessage => Node <%s> publishing message '%s' to area <%d,%d,%d>" % (senderID, payload, area.position[0], area.position[1],area.radius))
            self.publishSpatial(senderID, area, payload)
        if (type == 'join'):
            self.nodeID = message.getNodeID()
            IP = self.networkInterface.getIP()
            port = self.networkInterface.getPort()
            self.VAST.join(IP, port, self.nodeID)
            registeredNodes = message.getRegisteredNodes()
            for nodeID in registeredNodes:
                (nodeIP, nodePort) = registeredNodes[nodeID]
                self.VAST.join(nodeIP, nodePort, nodeID)
            logging.info("Matcher::handleMessage => MatcherNode::handleMessage => Received nodeID <%s> from gateway" % self.nodeID)

    def addChannelSubscription(self, nodeID, channel):
        if (channel in self.channelSubscriptions):
            self.channelSubscriptions[channel].append(nodeID)
        else:
            self.channelSubscriptions[channel] = [nodeID]


    def removeChannelSubscription(self, nodeID, channel):
        if channel in self.channelSubscriptions:
            subscribers = self.channelSubscriptions[channel]
            if nodeID in subscribers:
                subscribers.remove(nodeID)
                self.channelSubscriptions[channel] = subscribers


    def publishChannel(self, senderID, channel, payload):
        if channel in self.channelSubscriptions:
            subscribers = self.channelSubscriptions[channel]
            for subscriber in subscribers:
                msg = Message(senderID, type='deliverpub', channel=channel, payload=payload)
                self.send(subscriber, msg)


    def addSpatialSubscription(self, nodeID, area):
        foundSameArea = False
        for subscribedArea in self.spatialSubscriptions:
            if area.equal(subscribedArea):
                self.spatialSubscriptions[subscribedArea].append(nodeID)
                foundSameArea = True
        if (foundSameArea == False):
            self.spatialSubscriptions[area] = [nodeID]


    def removeSpatialSubscription(self, nodeID, area):
        for subscribedArea in self.spatialSubscriptions:
            if area.equal(subscribedArea):
                subscribers = self.spatialSubscriptions[subscribedArea]
                if nodeID in subscribers:
                    subscribers.remove(nodeID)
                    self.spatialSubscriptions[subscribedArea] = subscribers


    def publishSpatial(self, senderID, area, payload):
        for subscribedArea in self.spatialSubscriptions:
            if (area.overlap(subscribedArea) == 1):
                subscribers = self.spatialSubscriptions[subscribedArea]
                for subscriber in subscribers:
                    msg = Message(senderID, type='deliverpub')
                    msg.setArea(area)
                    msg.setPayload(payload)
                    self.send(subscriber, msg)


    def processSingleMessage(self):
        logging.debug("Matcher::processSingleMessage => <%d> messages in queue" % self.networkInterface.getNumberOfMessages())
        if (self.networkInterface.getNumberOfMessages()):
            message = self.networkInterface.getMessage()
            self.handleMessage(message)
            logging.info(self.getChannelSubscriptions())
            for subscribedArea in self.spatialSubscriptions:
                (x,y) = subscribedArea.position
                r = subscribedArea.radius
                logging.info("Matcher::processSingleMessage => defaultdict(None, {'(%d,%d,%d)': %s})" % (x, y, r, self.spatialSubscriptions[subscribedArea]))


    def processMessages(self):
        logging.debug("Matcher::processMessages => <%d> messages in queue" % self.networkInterface.getNumberOfMessages())
        while (self.networkInterface.getNumberOfMessages()):
            message = self.networkInterface.getMessage()
            self.handleMessage(message)
            logging.info(self.getChannelSubscriptions())
            for subscribedArea in self.spatialSubscriptions:
                (x,y) = subscribedArea.position
                r = subscribedArea.radius
                logging.info("Matcher::processMessages => defaultdict(None, {'(%d,%d,%d)': %s})" % (x, y, r, self.spatialSubscriptions[subscribedArea]))


    def getChannelSubscriptions(self):
        return self.channelSubscriptions


    def getSpatialSubscriptions(self):
        return self.spatialSubscriptions