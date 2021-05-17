from signalslot import *
from collections import defaultdict
import time
import threading

from Sender import *
from Receiver import *



def thread_function(node):
    for _ in range(2):
        time.sleep(1)
        node.send(msg=Message(type='pub',channel='ab', payload='message in thread'))
        

def main():
    nodes = [Node(id='1'), Node(id='2'), Node(id='4')]
    matcher = Matcher(id='3')
    
    # nodes connect to matcher
    for node in nodes:
        matcher.connect(node) #fix

    nodes[0].send(msg=Message(type='sub',channel='ab'))
    nodes[1].send(msg=Message(type='sub',channel='ab'))
    nodes[2].send(msg=Message(type='pub',channel='ab', payload='this is the first message'))

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