import sys
import getopt


from Node import VASTNode
from VAST import VASTInterface
from Message import Message
from Connector import *
import random

messageProcessingTick = 0.001


async def processReceiveMessage(node):
    while True:
        await asyncio.sleep(messageProcessingTick)
        node.processSingleMessage()


async def publishMessage(node, channel, subchannel, destinationID, messageNumber):
    subscribed = False
    while True:
        publishTick = random.randint(0, 2)
        await asyncio.sleep(publishTick)
        if (node.getNodeID() != None):
            logging:info("Have received nodeID <%s>" % node.getNodeID())
            if (subscribed == False):
                # Node '1' subscribes to channel 'test2'
                message = Message(senderNodeID=node.getNodeID(), type='sub', channel=subchannel, payload=None)
                node.send(destinationNodeID=0, message=message)
                subscribed = True
            else:

                payload = 'publication message %d' % messageNumber
                message = Message(senderNodeID=node.getNodeID(), type='pub', channel=channel, payload=payload)
                node.send(destinationNodeID=destinationID, message=message)
                messageNumber += 1

def main(argv):

    IP = ''
    port = ''
    subchannel = ''
    pubchannel = ''
    try:
        opts, args = getopt.getopt(argv, "hi:p:c:s:")
    except getopt.GetoptError:
        print
        'singlenode.py -i <IP address> -p <port>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print
            'singlenode.py -i <IP address> -p <port>'
            sys.exit()
        elif opt in ("-i"):
            IP = arg
        elif opt in ("-p"):
            port = int(arg)
        elif opt in ("-c"):
            pubchannel = arg
        elif opt in ("-s"):
            subchannel = arg


    print('(IP:Port) = (%s:%d)' % (IP, port))

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    gatewayIP = '127.0.0.1'
    gatewayPort = 49152

    VAST = VASTInterface()
    matcherNodeID = 0
    #VAST.join('127.0.0.1', 49153, matcherNodeID)
    #VAST.join('127.0.0.1', 49154, 1)
    #VAST.join('127.0.0.1', 49155, 2)


    node = VASTNode(networkInterface=RealNetworkInterface(senderIP=IP, senderPort=port), VASTInterface=VAST)
    node.initialiseNetworkInterface()
    node.registerID(gatewayIP, gatewayPort)


    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(processReceiveMessage(node))
        asyncio.ensure_future(publishMessage(node, pubchannel, subchannel, matcherNodeID, 0))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        logging.info("Closing Loop")

        loop.close()

if __name__ == '__main__':
    main(sys.argv[1:])