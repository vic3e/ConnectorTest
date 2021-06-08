import math

class Area(object):


    def __init__(self, position=(0,0), radius=0):
        self.position = position
        self.radius = radius


    def setRadius(self, radius):
        self.radius = radius


    def setPosition(self, position):
        self.position = position


    def equal(self, area):
        x1 = self.position[0]
        y1 = self.position[1]
        x2 = area.position[0]
        y2 = area.position[1]
        r1 = self.radius
        r2 = area.radius
        return ((x1 == x2 ) and (y1 == y2) and (r1 == r2))


    def overlap(self, area):
        x1 = self.position[0]
        y1 = self.position[1]
        x2 = area.position[0]
        y2 = area.position[1]
        r1 = self.radius
        r2 = area.radius

        d = math.sqrt(((x1-x2)**2)+((y1-y2)**2))

        rn = r1+r2

        if d < rn:
            result = 1
        elif d == rn:
            result = 0
        else:
            result = -1

       # print ("(x1,y1,r1) = (%d,%d,%d) and (x2,y2,r2) = (%d,%d,%d): %d" % (x1, y1, r1, x2, y2, r2, result))
        return result


    def key(self):
        x = self.position[0]
        y = self.position[1]
        r = self.radius
        return (x, y, r)