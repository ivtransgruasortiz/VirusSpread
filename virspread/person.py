# Module person.py
# The class that defines people

import random


class Person:
    # Initial initialization method
    def __init__(self, pos=[0, 0, 0], dist=10, paso=1, initio=True):
        self.pos = pos
        self.paso = paso
        self.initio = initio
        self.dist = dist
        self.pos_x = random.randint(self.pos[0], self.dist)
        self.pos_y = random.randint(self.pos[1], self.dist)
        self.pos_z = random.randint(self.pos[2], self.dist)

    # Returns the position of a individual person
    def pos_paso(self):
        if self.initio:
            position = [self.pos_x, self.pos_y, self.pos_z]
        else:
            rx = random.randint(-1, 1) * self.paso
            ry = random.randint(-1, 1) * self.paso
            rz = random.randint(-1, 1) * self.paso

            print(rx, ry, rz)

            px = self.pos[0] + rx
            py = self.pos[1] + ry
            pz = self.pos[2] + rz

            # if (px >= 0) and (px < self.dist):
            #     px = px
            # else:
            #     px = abs(abs(px) - self.dist)

            px = px if ((px >= 0) & (px < self.dist)) else abs(abs(px) - self.dist)
            py = py if ((py >= 0) & (py < self.dist)) else abs(abs(py) - self.dist)
            pz = pz if ((pz >= 0) & (pz < self.dist)) else abs(abs(pz) - self.dist)

            position = [px, py, pz]
        return position


list_persons = [Person() for i in range(3)]
len(list_persons)
print('INIT = ', list_persons[0].pos_paso())

for i in range(10):
    list_persons = [Person(pos=x.pos_paso(), initio=False) for x in list_persons]
    print(list_persons[0].pos_paso())
