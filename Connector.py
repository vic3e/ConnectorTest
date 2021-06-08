from abc import ABC, abstractmethod
from copy import deepcopy
import queue
import socket

import logging

interfaces = {} # dictionary to store interfaces -> {"IP:Port", "NetworkInterface"}


class NetworkInterface(ABC):


    @abstractmethod
    def connect(self, destinationIP, destinationPort):
        pass



    @abstractmethod
    def send(self, message):
        pass


    @abstractmethod
    def receive(self, message):
        pass


    @abstractmethod
    def bind(self):

        pass

    @abstractmethod
    def getIP(self):
        pass


    @abstractmethod
    def getPort(self):
        pass


    @abstractmethod
    def getNumberOfMessages(self):
        pass


    @abstractmethod
    def getMessage(self):
        pass


class RealNetworkInterface(NetworkInterface):
    def __init__(self, senderIP, senderPort):
        self.senderIP = senderIP
        self.senderPort = senderPort
        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiveQueue = queue.Queue()

    def connect(self, destinationIP, destinationPort):
        self.clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def send(self, message):
        self.clientSock.sendto( (UDP_IP_ADDRESS, UDP_PORT_NO))
        pass


    def receive(self, message):
        pass


    def bind(self):
        serverSock.bind(self.senderIP, self.senderPort)
        pass


    def getIP(self):
        pass


    def getPort(self):
        pass


    def getNumberOfMessages(self):
        pass


    def getMessage(self):
        pass


class FakeNetworkInterface(NetworkInterface):


    def __init__(self, senderIP, senderPort):
        self.senderIP = senderIP
        self.senderPort = senderPort
        self.receiveQueue = queue.Queue()


    def connect(self, destinationIP, destinationPort):
        logging.debug("Connecting (%s:%s) to (%s:%s)" % (self.senderIP, self.senderPort, destinationIP, destinationPort))
        self.destinationInterface = interfaces[destinationIP+":"+destinationPort]


    def bind(self):
        logging.info("FakeNetworkInterface::bind => Registering (IP:Port) = (%s:%s )" % (self.senderIP, self.senderPort))
        interfaces[self.senderIP+":"+self.senderPort] = self


    def send(self, message):
        logging.debug("Sending message '%s' to destinationInterface (%s:%s)" % (message, self.destinationInterface.getIP(), self.destinationInterface.getPort()))
        self.destinationInterface.receive(deepcopy(message))


    def receive(self, message):
        logging.debug("Receive Queue of NIC (%s:%s) has <%d> messages" % (self.senderIP, self.senderPort, self.receiveQueue.qsize()))
        self.receiveQueue.put(message)
        logging.debug("Receive Queue of NIC (%s:%s) has <%d> messages" % (self.senderIP, self.senderPort, self.receiveQueue.qsize()))


    def getIP(self):
        return self.senderIP


    def getPort(self):
        return self.senderPort


    def getNumberOfMessages(self):
        return self.receiveQueue.qsize()


    def getMessage(self):
        return self.receiveQueue.get()
