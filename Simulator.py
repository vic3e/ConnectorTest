from signalslot import *
from collections import defaultdict
import time
import threading

from Sender import *
from Receiver import *

from message import *

def thread_function(node):
    for _ in range(1):
        time.sleep(2)
        # node.send(msg=Message(type='pub',channel='ab', payload='message in thread'))
        node.send(msg=Message(type='pub', location=Location(25,15,10), payload='message in thread'))
        

def main():
    nodes = [Node(id='1'), Node(id='2'), Node(id='4'), Node(id='5'), Node(id='6'), Node(id='7')]
    matcher = Matcher(id='3')
    
    # matcher = Matcher(id='7', coverage=(100,-100))
    
    # nodes connect to matcher
    for node in nodes:
        matcher.connect(node) #fix

    # nodes[0].send(msg=Message(type='sub',channel='ab'))
    # nodes[1].send(msg=Message(type='sub',channel='ab'))
    
    nodes[3].send(msg=Message(type='sub', location=Location(15,15,10)))
    # nodes[4].send(msg=Message(type='sub', location=Location(45,15,10)))
    
    # nodes[2].send(msg=Message(type='pub', channel='ab', payload='this is node channel pub message'))    

    nodes[5].send(msg=Message(type='pub', location=Location(25,15,10), payload='this is node Spatial message')) #fix location, change to location, format is (x,y,r)


    threads = []

    for node in nodes:
        x = threading.Thread(target=thread_function, args=(node,))
        threads.append(x)
        x.start()

    for thread in threads:
        thread.join()



if __name__ == '__main__':
    main()
    print('program exitted')
