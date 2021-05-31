from signalslot import *
from collections import defaultdict
import time
import threading
import math

class Matcher(object):
    def __init__(self, id):
        self.lock = threading.Lock()
        self.id = id
        self.channel_signals = {} # {'channel': <signal_for_channel> }
        self.nodes = {} # {'node.id': <node> }
        self.subscriber_ids = {}
        self.publisher_ids = {}

        


    def handle_message(self,message, **kwargs):
        
        # print ('these are the node lists', self.nodes('radius'), 'and these are the channel signals', self.channel_signals)

        with self.lock:
            mc = message.channel
            mp = message.position
            mr = message.radius


            if message.type == 'sub':
                if mc not in self.channel_signals: # to avoid existing channel signal to be recreated/check for duplicate
                    self.channel_signals[mc] = Signal()
                    self.nodes[message.sender_id].can_publish(False) # for test only
                    self.channel_signals[mc].connect(self.nodes[message.sender_id].get_slot())
                    print(f'subscriber: {message.sender_id} makes request to channel: {mc}')
                else:
                    print(f'subscriber id: {message.sender_id} to channel: {mc}')
                    self.channel_signals[mc].connect(self.nodes[message.sender_id].get_slot())
                    self.nodes[message.sender_id].can_publish(False) # for test only
            
            elif message.type == 'pub':
                if mc in self.channel_signals:
                    print(f'publisher id: {message.sender_id} to channel: {mc}')
                    self.channel_signals[mc].emit(message = message)

            elif message.type == 'spatialsub':
                if mp not in self.channel_signals: # to avoid existing channel signal to be recreated/check for duplicate
                    self.channel_signals[mp] = Signal()
                    self.nodes[message.sender_id].can_publish(False) # for test only
                    self.channel_signals[mp].connect(self.nodes[message.sender_id].get_slot())
                    # self.overlap() - overlap check

                    #get 
                    print(f'\nSpatial subscriber id: {message.sender_id} at location {mp} with radius {message.radius} makes request')
                else:
                    print(f'\nSpatial subscriber id: {message.sender_id} at location {mp} with radius {message.radius} makes request')
                    self.channel_signals[mc].connect(self.nodes[message.sender_id].get_slot())
                    self.nodes[message.sender_id].can_publish(False) # for test only
            
            elif message.type == 'spatialpub':
                # Check
                print(f'radius is: {message.radius}, and  position is {message.position}, where x is {message.position[0]} and y is {message.position[1]}')
                if mc in self.channel_signals:
                    print(f'Spatial publisher id: {message.sender_id} to area: {mc}')
                    self.channel_signals[mc].emit(message = message)

                    
            else:
                print('unknown message type')
    
    def connect(self, node):
        node.connect(self.handle_message) # allows all nodes (publishers and subscribers) to call handle_message() slot     
        self.nodes[node.get_id()] = node # -this means that subs can publish so long they have the right channel


    def overlap(self, x1, x2, y1, y2, r1, r2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.r1 = r1
        self.r2 = r2

        d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        print(d)
        
        rn = r1 +r2
        print(rn)
        
        if d < rn:
            print('Node area 1 overlaps with Node area 2')
        
        elif d == rn:
            print("Nodes are touching")
            
        elif d > rn:
            print ("Nodes do not overlap, no match")

class Message(object):
    def __init__(self, type, channel='', payload='', id='', position=(), radius=''):
        self.sender_id = id # needed?
        self.type = type
        self.channel = channel
        self.payload = payload
        self.position = position
        self.radius = radius

    def set_id(self, id):
        self.sender_id = id
