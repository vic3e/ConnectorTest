import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
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

n2_cor = (30, 25)
n2_rad = 10


n3_cor = (30, 50)
n3_rad = 15


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

if  (n1_cor <= (120, 100)):# and n2_cor[1] <= n2_cor[2]:
    print ('match found in matcher 1 area')
else:    
    print ('no match')
    
    
if (n2_cor <= (240, 100)):
    print ('match found in matcher 2 area')
else:
    print('no match found in matcher 2')
    

    
    
# circle = plt.Circle((0, 0), 0.75, fc='y')
# plt.gca().add_patch(circle)

# plt.axis('scaled')
# plt.show()
