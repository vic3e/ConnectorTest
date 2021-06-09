import sys
import getopt


from Node import MatcherNode
from Node import VASTNode, SPSNode
from VAST import VASTInterface
from Message import Message
from Connector import *
from Area import Area


messageProcessingTick = 0.001
simulationTick = 0.01

async def processReceiveMessage(node):
    while True:
        await asyncio.sleep(messageProcessingTick)
        node.processSingleMessage()

def main(argv):


    IP = ''
    port = ''
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
        elif opt in ("-ip"):
            IP = arg
        elif opt in ("-port"):
            port = int(arg)

    print('(IP:Port) = (%s:%d)' % (IP, port))

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    VAST = VASTInterface()
    matcherNodeID = 12000
    VAST.join(matcherNodeID, '127.0.0.1',12000)
    VAST.join(12001, '127.0.0.1',12001)
    VAST.join(12002, '127.0.0.1',12002)

    matcher = MatcherNode(nodeID=matcherNodeID, networkInterface=RealNetworkInterface(senderIP=IP, senderPort=12000), VASTInterface=VAST)
    matcher.registerID()

    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(processReceiveMessage(matcher))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        logging.info("Closing Loop")

        loop.close()

if __name__ == '__main__':
    main(sys.argv[1:])