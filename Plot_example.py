import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import math
# from shapely.geometry import box


#Matcher Coordinates
m1_cor = (0,0) #position
m1x1 = 120  #length
m1y1 = 100 #breadth


m2_cor = (120,0) #position
m2x1 = 120
m2x2 = 100

# Node coordinates
n1_cor = (15,15)
# print(n1_cor[1])
n1_rad = 10

n2_cor = (25, 15)
n2_rad = 10


n3_cor = (45, 15)
n3_rad = 10


plt.axes()

matcher_one = plt.Rectangle(m1_cor, m1x1, m1y1)
matcher_two = plt.Rectangle(m2_cor, m2x1, m2x2, fc='r')


node1 = plt.Circle(n1_cor, n1_rad, fc='y')
node2 = plt.Circle(n2_cor, n2_rad, fc='g')
node3 = plt.Circle(n3_cor, n3_rad, fc='w')

# print(node1[1])

plt.gca().add_patch(matcher_one)
# plt.gca().add_patch(matcher_two)

plt.gca().add_patch(node1)
plt.gca().add_patch(node2)
plt.gca().add_patch(node3)

plt.axis('scaled')
plt.show()


def overlap(x1, x2, y1, y2, r1, r2):
    
    d = math.sqrt(abs((x1-x2))**2 + abs((y1-y2)**2))
    print(d)
    
    rn = r1 +r2
    print(rn)
    
    if d < rn:
        print('Node area 1 overlaps with Node area 2')
    
    elif d == rn:
        print("Nodes are touching, no match")
        
    elif d > rn:
        print ("Nodes do not overlap, no match")
    
overlap(15, 25, 15, 15, 10, 10)    
    
# circle = plt.Circle((0, 0), 0.75, fc='y')
# plt.gca().add_patch(circle)

# plt.axis('scaled')
# plt.show()
