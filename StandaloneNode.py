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


async def publishMessage(node, channel, destinationID, messageNumber):
    while True:
        publishTick = random.randint(0,2)
        await asyncio.sleep(publishTick)
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

    VAST = VASTInterface()
    matcherNodeID = 12000
    VAST.join(matcherNodeID, '127.0.0.1',12000)
    VAST.join(12001, '127.0.0.1',12001)
    VAST.join(12002, '127.0.0.1',12002)

    node = VASTNode(nodeID=port, networkInterface=RealNetworkInterface(senderIP=IP, senderPort=port), VASTInterface=VAST)
    node.registerID()

    # Node '1' subscribes to channel 'test2'
    message = Message(senderNodeID=node.getNodeID(), type='sub', channel=subchannel, payload=None)
    node.send(destinationNodeID=matcherNodeID, message=message)


    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(processReceiveMessage(node))
        asyncio.ensure_future(publishMessage(node, pubchannel, matcherNodeID, 0))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        logging.info("Closing Loop")

        loop.close()

if __name__ == '__main__':
    main(sys.argv[1:])