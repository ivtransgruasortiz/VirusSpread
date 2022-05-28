# Module person.py
# The class that defines people

import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time

# Constants
min, max = -10, 20
pasos = 200
num_pers = 50
pause = 0.01
value_height = 10
value_width = 10
sizemarker = 80
# func_color = [random.choice(['r', 'b', 'g']) for x in dict_persons]
func_color = 'r'

class Person:
    # Initial initialization method
    def __init__(self, pos=None, dist=10, paso=1):
        self.paso = paso
        self.dist = dist
        if pos is None:
            pos_ini = [0, 0, 0]
            pos = list(map(lambda x: random.randint(x, self.dist), pos_ini))
        self.pos = pos
        # print('POS_INI')
        # print(self.pos)

    # Returns the position of a individual person
    def pos_new(self, last_pos=None):
        delta_pos = list(map(lambda x: random.randint(-1, 1) * self.paso, self.pos))
        # print('DELTA')
        # print(delta_pos)
        if last_pos is None:
            pos_paso = [sum(x) for x in zip(self.pos, delta_pos)]
        else:
            pos_paso = [sum(x) for x in zip(last_pos, delta_pos)]
        # print('POS_PASO')
        # print(pos_paso)
        # Circular edges
        pos_paso = [x if ((x >= 0) & (x < self.dist)) else abs(abs(x) - self.dist) for x in pos_paso]
        return delta_pos, pos_paso


# Initialization
list_persons = [Person() for i in range(num_pers)]
dict_persons = [{"pos_ini": x.pos,
                 "last_pos": [0, 0, 0],
                 "pos_new": x.pos_new()[1],
                 } for x in list_persons]

# Evolution
fig = plt.figure()
fig.set_figheight(value_height)
fig.set_figwidth(value_width)
ax = plt.axes(projection='3d')

for i in range(pasos):
    dict_persons = [
        {"pos_ini": x.pos,
         "last_pos": y['pos_new'][1],
         "pos_new": x.pos_new(y['pos_new'])[1],
         }
        for x, y in zip(list_persons, dict_persons)]
    # graphs
    ax.clear()
    ax.set(xlim=(min, max), ylim=(min, max), zlim=(min, max))
    ax.scatter(np.array([x['pos_new'][0] for x in dict_persons]),
               np.array([x['pos_new'][1] for x in dict_persons]),
               np.array([x['pos_new'][2] for x in dict_persons]),
               zdir='z', s=sizemarker, c=func_color,
               depthshade=False,
               marker="H",
               )
    plt.pause(pause)






# PoC OK!!
a = Person()
pers_dicc = [
    {"pos_ini": a.pos,
     "last_pos": [0, 0, 0],
     "pos_new": a.pos_new(),
     }
]
pers_dicc = [
    {"pos_ini": a.pos,
     "last_pos": pers_dicc[0]['pos_new'][1],
     "pos_new": a.pos_new(pers_dicc[0]['pos_new'][1]),
     }
]

