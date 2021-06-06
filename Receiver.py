from signalslot import *
# from collections import defaultdict
from collections import namedtuple
import time
import threading
import math

from message import *
LocationId =  namedtuple('LocationId', 'node_id location') # workaround for now

class Matcher(object):
    def __init__(self, id):
        self.lock = threading.Lock()
        self.id = id
       
        self.channel_signals = {} # {'channel': <signal_for_channel> }

        self.nodes = {} # {'node.id': <node> }

        self.subscriber_locations = []
        # self.publisher_ids = {}

        # self.spatialsublist = {}
        


    def handle_message(self,message, **kwargs):
        
        # print ('these are the node lists', self.nodes, 'and these are the channel signals', self.channel_signals)

        #with self.lock:
        mc = message.channel
            
            # mp = message.position
            # mr = message.radius

        if message.type == 'sub':
               #append to sub dictionary
            if mc == '':
                print('spatial sub saved')
                self.subscriber_locations.append(LocationId(node_id=message.sender_id, location=message.location)) # {subscriber identification: 1, location}

            if mc not in self.channel_signals and mc: # to avoid existing channel signal to be recreated/check for duplicate
                self.channel_signals[mc] = Signal()
                self.nodes[message.sender_id].can_publish(False) # for test only
                self.channel_signals[mc].connect(self.nodes[message.sender_id].get_slot())
                print(f'subscriber: {message.sender_id} makes request to channel: {mc}')

            elif mc in self.channel_signals:
                print(f'subscriber id: {message.sender_id} to channel: {mc}')
                self.channel_signals[mc].connect(self.nodes[message.sender_id].get_slot()) #connect signal to slot
                self.nodes[message.sender_id].can_publish(False) # for test only
            
        elif message.type == 'pub':
            if mc == '':
                for subloc in self.subscriber_locations:
                    print('SUB', subloc)
                    if self.overlap(subloc.location, message.location):
                        publisher = self.nodes.get(message.sender_id) # get pub from nodes
                        subscriber = self.nodes.get(subloc.node_id)
                        print('SUBSCR:', subscriber)
                        print('PUBL: ', publisher)
                        

                        if publisher is not None and subscriber is not None:
                            print('in if for: ')
                            print('in if for: ')

                            publisher.connect(subscriber.get_slot())
                            print('exit if slot: ')

                            # with self.lock:
                            # publisher.send(msg=message)
                            # print('exit if for: ')
                            




             # if mc not in sub dictionary, do nothing
             # else perform matching
                if mc in self.channel_signals:
                    print(f'publisher id: {message.sender_id} to channel: {mc}')
                    self.channel_signals[mc].emit(message = message)

                    
            else:
                print('unknown message type')
    

    def connect(self, node):
        node.connect(self.handle_message) # allows all nodes (publishers and subscribers) to call handle_message() slot     
        self.nodes[node.get_id()] = node # -this means that subs can publish so long they have the right channel


    def overlap(self, node_one_location, node_two_location): #change variable names

        d = math.sqrt(abs(node_one_location.x_position - node_two_location.x_position)**2 + abs(node_one_location.y_position - node_two_location.y_position)**2)
        # print(d)
        
        rn = node_one_location.radius + node_two_location.radius
        print(f'd is {d} and rn is {rn}')
        
        if d < rn:
            # print('Node area 1 overlaps with Node area 2')
            return True # this is the interesting part
        elif d == rn:
            # print("Nodes are touching")
            return False
            
        elif d > rn:
            # print ("Nodes do not overlap, no match")
            return False


