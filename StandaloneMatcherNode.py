import sys
import getopt


from Node import MatcherNode
from VAST import VASTInterface
from Connector import *


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
        opts, args = getopt.getopt(argv, "hi:p:")
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

    gatewayIP = '127.0.0.1'
    gatewayPort = 49152

    VAST = VASTInterface()
    #matcherNodeID = 0
    #VAST.join('127.0.0.1', 49153, matcherNodeID)
    #VAST.join('127.0.0.1', 49154, 1)
    #VAST.join('127.0.0.1', 49155, 2)

    matcher = MatcherNode(networkInterface=RealNetworkInterface(senderIP=IP, senderPort=49153), VASTInterface=VAST)
    matcher.initialiseNetworkInterface()
    matcher.registerID(gatewayIP, gatewayPort)

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