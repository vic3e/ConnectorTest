from collections import namedtuple

Location = namedtuple("Location", "x_position y_position radius")


class Message(object): # POD - plain old data
    def __init__(self, type, channel='', payload='', id='',location=None):
        self.sender_id = id # needed?
        self.type = type
        self.channel = channel
        self.payload = payload
        # self.position = position
        # self.radius = radius
        self.location = location

    def set_id(self, id):
        self.sender_id = id



