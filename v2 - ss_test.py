from signalslot import *
from collections import defaultdict
import time
import threading
import string
import random

class Node(object):
    def __init__(self, message1, id, channel):
        self.signal = Signal() #signal
        self.id = id
        self.channel = channel
        self.slot = self.receive
        self.message1 = message1

    def get_id(self):
        return self.id

    def get_message1(self):
        return self.message1

    def receive(self, message, **kwargs): #slot
        print(f'subscriber id:{self.id} and got: ', message)
    
    def send(self, msg):
        self.signal.emit(message = msg)

    def get_slot(self):
        return self.receive
    
    def get_channel(self):
        return self.channel

    def connect(self, func):
        return self.signal.connect(func)

    def messagegenerator():
        return
        
    def publish(self):
        return
    
    def subscribe(self):
        return

# matcher
class Matcher(object):
    def __init__(self):
        self.id = '3'
        self.subscribers = defaultdict(list)
        # self.publishers = defaultdict(list)

    def store_or_match(self, node):       # v = 

        if node.get_message1() == None: #sub request
            # self.subscribers = defaultdict(list)
            
            c1 = node.get_channel()
            print('this is sub c1', c1)
            # c1 = publisher.get_channel()

            # for publisher in self.publishers[c]:
            #     if publisher.get_channel() == c:
            #         publisher.connect(node.get_slot()) # subscribe to different pubs
            # else:
            #     self.subscribers[c].append(node)

        if node.get_message1() == 'pub':
            c = node.get_channel()
            print('this is pub c', c)

            for subscriber in self.subscribers[c]:
                n1 = subscriber.get_channel()
                
                if n1 == c:
                    print('this is n1 and c', n1, c)
                    node.connect(subscriber.get_slot())
                    # publisher.connect(node.get_slot())
                    # self.publishers[c].append(node)
                    
            else:
                print('no match')
                # self.publishers[c].append(node) 
            


def publishing_function(publisher):
    print('node id ', publisher.get_id())
    if publisher.get_message1() == 'pub':
        while True:
            message = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
            time.sleep(1)
            publisher.send(msg=message)
        

def main():
    nodes = [Node(message1=None, id='1', channel='as'), Node(message1='pub', id='5', channel='ab'),Node(message1=None, id='6', channel='ab')]
    matcher = Matcher()
    
    for node in nodes:
        matcher.store_or_match(node)
    
    threads = [] # []

    for node in nodes:
        x = threading.Thread(target=publishing_function, args=(node,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()


if __name__ == '__main__':
    main()
    print('program exitted')

    