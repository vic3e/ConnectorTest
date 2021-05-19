from signalslot import *
from collections import defaultdict
import time
import threading


class Node(object):
    def __init__(self, id):
        self.signal = Signal()
        self.id = id
        self.slot = self.receive
        self.is_publisher = True

    def connect(self, func): # connect to a matcher
        return self.signal.connect(func)

    def send(self, msg):
        if self.is_publisher:
            msg.set_id(self.id)
            self.signal.emit(message = msg)
    
    def receive(self, message, **kwargs):
        print(f'Node id {self.id} received: "{message.payload}" from Node id: {message.sender_id}')

    def get_id(self):
        return self.id

    def get_slot(self):
        return self.receive

    def can_publish(self, state):
        self.is_publisher = state
    
    # def publish(self):
    #     if self.state == 'pub':
    #     #publish a message function
    #     return get_id, channel, Message

class Message(object):
    def __init__(self, type, channel='', payload='', id='', area=''):
        self.sender_id = id # needed?
        self.type = type
        self.channel = channel
        self.payload = payload
        self.area = area

    def set_id(self, id):
        self.sender_id = id
    
    def nodearea(self):
        return self.radius**2*3.14
    
    def perimeter(self):
        return 2*self.radius*3.14
