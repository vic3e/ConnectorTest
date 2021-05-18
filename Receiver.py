from signalslot import *
from collections import defaultdict
import time
import threading


class Matcher(object):
    def __init__(self, id):
        self.lock = threading.Lock()
        self.id = id
        self.channel_signals = {} # {'channel': <signal_for_channel> }
        self.nodes = {} # {'node.id': <node> }
        self.subscriber_ids = {}
        self.publisher_ids = {}


    def handle_message(self,message, **kwargs):
        
        with self.lock:
            mc = message.channel
            if message.type == 'sub':
                if mc not in self.channel_signals: # to avoid existing channel signal to be recreated/check for duplicate
                    self.channel_signals[mc] = Signal()
                    self.nodes[message.sender_id].can_publish(False) # for test only
                    self.channel_signals[mc].connect(self.nodes[message.sender_id].get_slot())
                    print(f'subscriber id: {message.sender_id} to channel: {mc}')
                else:
                    print(f'subscriber id: {message.sender_id} to channel: {mc}')
                    self.channel_signals[mc].connect(self.nodes[message.sender_id].get_slot())
                    self.nodes[message.sender_id].can_publish(False) # for test only
            
            elif message.type == 'pub':
                if mc in self.channel_signals:
                    print(f'publisher id: {message.sender_id} to channel: {mc}')
                    self.channel_signals[mc].emit(message = message)


            elif message.type == 'spatialsub':
                if mc not in self.channel_signals: # to avoid existing channel signal to be recreated/check for duplicate
                    self.channel_signals[mc] = Signal()
                    self.nodes[message.sender_id].can_publish(False) # for test only
                    self.channel_signals[mc].connect(self.nodes[message.sender_id].get_slot())
                    print(f'\nSpatial subscriber id: {message.sender_id} to area code: {mc}')
                else:
                    print(f'\nSpatial subscriber ids: {message.sender_id} to area code: {mc}')
                    self.channel_signals[mc].connect(self.nodes[message.sender_id].get_slot())
                    self.nodes[message.sender_id].can_publish(False) # for test only
            
            elif message.type == 'spatialpub':
                if mc in self.channel_signals:
                    print(f'Spatial publisher id: {message.sender_id} to area: {mc}')
                    self.channel_signals[mc].emit(message = message)

            else:
                print('unknown message type')
    
    def connect(self, node):
        node.connect(self.handle_message) # allows all nodes (publishers and subscribers) to call handle_message() slot     
        self.nodes[node.get_id()] = node # -this means that subs can publish so long they have the right channel


class Message(object):
    def __init__(self, type, channel, payload='', id=''):
        self.sender_id = id # needed?
        self.type = type
        self.channel = channel
        self.payload = payload

    def set_id(self, id):
        self.sender_id = id