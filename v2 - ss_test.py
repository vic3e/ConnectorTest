from signalslot import *
from collections import defaultdict
import time
import threading
import string
import random

class Node(object):
    def __init__(self, mission, id, channel):
        self.signal = Signal() #signal
        self.id = id
        self.channel = channel
        self.slot = self.receive
        self.mission = mission

    def get_id(self):
        return self.id

    def get_mission(self):
        return self.mission

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

# matcher
class Matcher(object):
    def __init__(self):
        self.id = '3'
        self.subscribers = defaultdict(list)
        self.publishers = defaultdict(list)

    def store_or_match(self, node):
        if node.get_mission() == 'sub':
            c = node.get_channel()

            for publisher in self.publishers[c]:
                if publisher.get_channel() == c:
                    publisher.connect(node.get_slot()) # subscribe to different pubs
            else:
                self.subscribers[c].append(node)

        elif node.get_mission() == 'pub':
            c = node.get_channel()

            for subscriber in self.subscribers[c]:
                if subscriber.get_channel() == c:
                    node.connect(subscriber.get_slot())
            else:
                self.publishers[c].append(node) 
            


def publishing_function(publisher):
    print('node id ', publisher.get_id())
    if publisher.get_mission() == 'pub':
        while True:
            message = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
            time.sleep(1)
            publisher.send(msg=message)
        

def main():
    nodes = [Node(mission='sub', id='1', channel='ba'), Node(mission='pub', id='5', channel='ab'),Node(mission='sub', id='6', channel='ab')]
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

    