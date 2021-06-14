
import logging
import asyncio

from Node import MatcherNode
from Node import VASTNode, SPSNode, Gateway
from VAST import VASTInterface
from Message import Message
from Connector import *
from Area import Area

simulationTick = 0.01
messageProcessingTick = 0.001

async def work(node):
    while True:
        await asyncio.sleep(messageProcessingTick)
        node.processSingleMessage()


async def simulate(matcher, nodes, loop):
    await asyncio.sleep(2)
    matcherNodeID = matcher.getNodeID()

    # Channel based pub/sub
    logging.info("")
    logging.info("Simulator::main => TESTING CHANNEL-BASED PUB/SUB")
    logging.info("")

    # Node '0' subscribes to channel 'test'
    message = Message(senderNodeID=matcher.getNodeID(), type='sub', channel='test', payload=None)
    matcher.send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    # Node '1' subscribes to channel 'test2'
    message = Message(senderNodeID=nodes[0].getNodeID(), type='sub', channel='test', payload=None)
    nodes[0].send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    # Node '1' subscribes to channel 'test2'
    message = Message(senderNodeID=nodes[1].getNodeID(), type='sub', channel='test2', payload=None)
    nodes[1].send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    message = Message(senderNodeID=nodes[1].getNodeID(), type='pub', channel='test2', payload='publication message 1')
    nodes[1].send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    message = Message(senderNodeID=nodes[0].getNodeID(), type='pub', channel='test2', payload='publication message 2')
    nodes[0].send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    message = Message(senderNodeID=nodes[1].getNodeID(), type='pub', channel='test', payload='publication message 3')
    nodes[1].send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    # Node '0' unsubscribes from channel 'test'
    message = Message(senderNodeID=matcher.getNodeID(), type='unsub', channel='test')
    matcher.send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    message = Message(senderNodeID=nodes[1].getNodeID(), type='pub', channel='test', payload='publication message 4')
    nodes[1].send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    # Node '0' unsubscribes from channel 'test'
    message = Message(senderNodeID=nodes[0].getNodeID(), type='unsub', channel='test')
    nodes[0].send(destinationNodeID=matcherNodeID, message=message)

    await asyncio.sleep(simulationTick)

    message = Message(senderNodeID=nodes[1].getNodeID(), type='pub', channel='test', payload='publication message 5')
    nodes[1].send(destinationNodeID=matcherNodeID, message=message)

    await asyncio.sleep(simulationTick)

    # Node '2' subscribes to channel 'test'
    message = Message(senderNodeID=nodes[1].getNodeID(), type='unsub', channel='test2')
    nodes[1].send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    # Spatial pub/sub

    logging.info("")
    logging.info("Simulator::main => TESTING SPATIAL PUB/SUB")
    logging.info("")

    # Node '0' subscribes to area (x,y,r)=(0,0,10)
    pos1 = (0, 0)
    radius1 = 10
    message = Message(senderNodeID=matcher.getNodeID(), type='spatialsub')
    message.setArea(area=Area(pos1, radius1))
    matcher.send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    # Node '1' subscribes to area (x,y,r)=(0,5,5)
    pos2 = (0, 5)
    radius2 = 5
    message = Message(senderNodeID=nodes[0].getNodeID(), type='spatialsub')
    message.setArea(area=Area(pos2, radius2))
    nodes[0].send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    # Node '2' subscribes to area (x,y,r)=(0,5,5)
    pos2 = (0, 5)
    radius2 = 5
    message = Message(senderNodeID=nodes[1].getNodeID(), type='spatialsub')
    message.setArea(area=Area(pos2, radius2))
    nodes[1].send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    # Node '1' publishes to area (x,y,r)=(0,5,1)
    pos2 = (0, 5)
    radius3 = 1
    message = Message(senderNodeID=nodes[0].getNodeID(), type='spatialpub')
    message.setArea(area=Area(pos2, radius3))
    message.setPayload(payload='spatial publication message 1')
    nodes[0].send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    # Node '2' unsubscribes from area (x,y,r)=(0,5,5)
    pos2 = (0, 5)
    radius2 = 5
    message = Message(senderNodeID=nodes[1].getNodeID(), type='spatialunsub')
    message.setArea(area=Area(pos2, radius2))
    nodes[1].send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    # Node '0' publishes to area (x,y,r)=(0,5,1)
    pos2 = (0, 5)
    radius3 = 1
    message = Message(senderNodeID=matcher.getNodeID(), type='spatialpub')
    message.setArea(area=Area(pos2, radius3))
    message.setPayload(payload='spatial publication message 2')
    matcher.send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    # Node '0' publishes to area (x,y,r)=(0,-5,1)
    pos3 = (0, -5)
    radius3 = 1
    message = Message(senderNodeID=matcher.getNodeID(), type='spatialpub')
    message.setArea(area=Area(pos3, radius3))
    message.setPayload(payload='spatial publication message 3')
    matcher.send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    # Node '0' publishes to area (x,y,r)=(0,20,1)
    pos4 = (0, 20)
    radius3 = 1
    message = Message(senderNodeID=matcher.getNodeID(), type='spatialpub')
    message.setArea(area=Area(pos4, radius3))
    message.setPayload(payload='spatial publication message 4')
    matcher.send(destinationNodeID=matcherNodeID, message=message)

    await asyncio.sleep(simulationTick)

    # Node '0' unsubscribes from area (x,y,r)=(0,0,10)
    pos1 = (0, 0)
    radius1 = 10
    message = Message(senderNodeID=matcher.getNodeID(), type='spatialunsub')
    message.setArea(area=Area(pos1, radius1))
    matcher.send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    # Node '1' unsubscribes from area (x,y,r)=(0,5,5)
    pos2 = (0, 5)
    radius2 = 5
    message = Message(senderNodeID=nodes[0].getNodeID(), type='spatialunsub')
    message.setArea(area=Area(pos2, radius2))
    nodes[0].send(destinationNodeID=matcherNodeID, message=message)
    await asyncio.sleep(simulationTick)

    logging.info("")
    logging.info("Simulator::Main => TESTING channel-based PUB/SUB using SPS clients")
    logging.info("")

    spsnodes = []

    for node in nodes:
        spsnodes.append(SPSNode(node, matcherNodeID))

    # SPS Node '1' subscribing to channel 'test3'
    spsnodes[0].subscribeToChannel('test3')
    await asyncio.sleep(simulationTick)

    # SPS Node '1' subscribing to channel 'test4'
    spsnodes[0].subscribeToChannel('test4')
    await asyncio.sleep(simulationTick)

    # SPS Node '2' subscribing to channel 'test3'
    spsnodes[1].subscribeToChannel('test3')
    await asyncio.sleep(simulationTick)

    # SPS Node '1' publishing to channel 'test3'
    spsnodes[0].publishToChannel('test3', 'SPS publication test 1')
    await asyncio.sleep(simulationTick)

    # SPS Node '1' publishing to channel 'test4'
    spsnodes[0].publishToChannel('test4', 'SPS publication test 2')
    await asyncio.sleep(simulationTick)

    # SPS Node '2' publishing to channel 'test4'
    spsnodes[1].publishToChannel('test4', 'SPS publication test 3')
    await asyncio.sleep(simulationTick)

    # SPS Node '2' publishing to channel 'test5' which has no subscribers
    spsnodes[1].publishToChannel('test5', 'SPS publication test 4')
    await asyncio.sleep(simulationTick)

    # SPS Node '1' unsubscribing to channel 'test3'
    spsnodes[0].unsubscribeFromChannel('test3')
    await asyncio.sleep(simulationTick)

    # SPS Node '1' unsubscribing from channel 'test4'
    spsnodes[0].unsubscribeFromChannel('test4')
    await asyncio.sleep(simulationTick)

    # SPS Node '2' unsubscribing from channel 'test3'
    spsnodes[1].unsubscribeFromChannel('test3')
    await asyncio.sleep(simulationTick)


    logging.info("")
    logging.info("Simulator::Main => TESTING spatial-based PUB/SUB using SPS clients")
    logging.info("")

    area1 = Area((0, 0), 10)
    area2 = Area((0, 5), 5)
    area3 = Area((0, 5), 1)
    area4 = Area((0, -5), 1)
    area5 = Area((0, 20), 1)

    # SPS Node '1' subscribing to area (0,0,10)
    spsnodes[0].subscribeToArea(area1)
    await asyncio.sleep(simulationTick)

    # SPS Node '1' subscribing to area (0,5,5)
    spsnodes[0].subscribeToArea(area2)
    await asyncio.sleep(simulationTick)

    # SPS Node '2' subscribing to area (0,0,10)
    spsnodes[1].subscribeToArea(area1)
    await asyncio.sleep(simulationTick)


    # SPS Node '1' publishing to area (0,5,1)
    spsnodes[0].publishToArea(area3, 'SPS area publication test 1')
    await asyncio.sleep(simulationTick)

    # SPS Node '1' publishing to area (0,-5,1)
    spsnodes[0].publishToArea(area4, 'SPS area publication test 2')
    await asyncio.sleep(simulationTick)

    # SPS Node '2' publishing to area (0,20,1)
    spsnodes[1].publishToArea(area5, 'SPS area publication test 3')
    await asyncio.sleep(simulationTick)

    # SPS Node '1' unsubscribing from area (0,0,10)
    spsnodes[0].unsubscribeFromArea(area1)
    await asyncio.sleep(simulationTick)

    # SPS Node '1' unsubscribing from area (0,5,5)
    spsnodes[0].unsubscribeFromArea(area2)
    await asyncio.sleep(simulationTick)

    # SPS Node '2' unsubscribing from area (0,0,10)
    spsnodes[1].unsubscribeFromArea(area1)
    await asyncio.sleep(simulationTick)

    loop.stop()


def main():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    gatewayIP = '127.0.0.1'
    gatewayPort = 10000

    VAST = VASTInterface()
    RealNetwork = True

    if (RealNetwork):
        gateway = Gateway(RealNetworkInterface(senderIP=gatewayIP, senderPort=gatewayPort))
        matcher = MatcherNode(networkInterface=RealNetworkInterface(senderIP='127.0.0.1', senderPort=12000), VASTInterface=VAST)
        nodes = [VASTNode(networkInterface=RealNetworkInterface(senderIP='127.0.0.1', senderPort=12001), VASTInterface=VAST),
                 VASTNode(networkInterface=RealNetworkInterface(senderIP='127.0.0.1', senderPort=12002), VASTInterface=VAST)]


    else:
        gateway = Gateway(RealNetworkInterface(senderIP=gatewayIP, senderPort=gatewayPort))
        matcher = MatcherNode(networkInterface=FakeNetworkInterface(senderIP='127.0.0.1', senderPort=12000),
                              VASTInterface=VAST)
        nodes = [VASTNode(networkInterface=FakeNetworkInterface(senderIP='127.0.0.1', senderPort=12001),
                          VASTInterface=VAST),
                 VASTNode(networkInterface=FakeNetworkInterface(senderIP='127.0.0.1', senderPort=12002),
                          VASTInterface=VAST)]

    # Initialise network interface
    gateway.initialiseNetworkInterface()
    matcher.initialiseNetworkInterface()
    for node in nodes:
        node.initialiseNetworkInterface()

    # Matcher obtain nodeID from gateway
    matcher.registerID(gatewayIP, gatewayPort)
    matcherNodeID = matcher.getNodeID()

    # Nodes obtain nodeIDs from gateway
    for node in nodes:
        node.registerID(gatewayIP, gatewayPort)

    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(work(matcher))
        asyncio.ensure_future(work(gateway))
        for node in nodes:
            asyncio.ensure_future(work(node))
        asyncio.ensure_future(simulate(matcher, nodes, loop))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        logging.info("Closing Loop")

        loop.close()


    logging.info('Simulator::main => Finished')

if __name__ == '__main__':
    main()