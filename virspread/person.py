# Module person.py
# The class that defines people

import random
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import time

# choices(population, weights)
# Constants
intervalo_random = [0, 1]  # Pegajosidad
weights = [.95, .05]  # Pegajosidad
min, max = -40, 40
# min, max = -110, 110  # maximos y minimos grafico
pasos = 500
num_pers = 500
pause = 0.0001
value_height = 10
value_width = 10
sizemarker = 70
# func_color = [random.choice(['r', 'b', 'g']) for x in dict_persons]  # Para el futuro
func_color = 'r'
dist_ini = 20  # limit para generacion espontanea
frontier = 100  # frontera real movimiento
paso_mov = 1
repulse = True
born_rate = 0.2
death_rate = 0.8


class Person:
    # Initial initialization method
    def __init__(self, pos=None, dist=dist_ini, paso=paso_mov):
        self.paso = paso
        self.dist = dist
        if pos is None:
            pos_ini = [0, 0, 0]
            pos = list(map(lambda x: random.randint(x, self.dist), pos_ini))
        self.pos = pos

    # Returns the position of a individual person

    def pos_new(self, last_pos=None):
        delta_pos = list(map(lambda x: random.randint(-1, 1) * self.paso, self.pos))
        # Movimento pegajoso
        # mov_pegajoso = random.choices(intervalo_random, weights)[0]
        # delta_pos = [x if (delta_pos.index(x) == 0) else x * mov_pegajoso for x in delta_pos]
        if last_pos is None:
            pos_paso = [sum(x) for x in zip(self.pos, delta_pos)]
        else:
            pos_paso = [sum(x) for x in zip(last_pos, delta_pos)]
        # Periodic boundaries
        # pos_paso = [x if ((x >= 0) & (x < self.dist)) else abs(abs(x) - self.dist) for x in pos_paso]
        pos_paso = [x if ((x >= -frontier) & (x < frontier)) else abs(abs(x) - 2 * frontier) for x in pos_paso]
        return delta_pos, pos_paso


def pisado(person_class, dict_persons_=None, last_position=None):
    if dict_persons_ is None:
        dict_persons_ = []
    result = person_class.pos_new(last_pos=last_position)[1]
    while result in [person_element["pos_new"] for person_element in dict_persons_]:
        result = person_class.pos_new(last_pos=last_position)[1]
    return result


def born(list_person, dict_person):
    x = Person()
    list_person.append(x)
    dict_person.append({"pos_ini": x.pos,
                        "last_pos": [0, 0, 0],
                        "pos_new": pisado(x, dict_persons),
                        })
    return list_person, dict_person


def death(list_person, dict_person):
    number = len(list_person)
    perca = random.randint(0, number - 1)
    list_person.pop(perca)
    dict_person.pop(perca)
    return list_person, dict_person


# Initialization
list_persons = [Person() for i in range(num_pers)]
dict_persons = []
for x in list_persons:
    dict_persons.append({"pos_ini": x.pos,
                         "last_pos": [0, 0, 0],
                         "pos_new": pisado(x, dict_persons),
                         })
# OLD
# dict_persons = [{"pos_ini": x.pos,
#                  "last_pos": [0, 0, 0],
#                  "pos_new": x.pos_new()[1],
#                  } for x in list_persons]

# Evolution
fig = plt.figure()
fig.set_figheight(value_height)
fig.set_figwidth(value_width)
ax = plt.axes(projection='3d')

while len(list_persons) > 0:
    for i in range(pasos):
        if not repulse:
            dict_persons = [
                {"pos_ini": x.pos,
                 "last_pos": y['pos_new'],
                 "pos_new": x.pos_new(y['pos_new'])[1],
                 }
                for x, y in zip(list_persons, dict_persons)]
        else:
            # Opcion con pisado
            for x, y in zip(list_persons, dict_persons):
                # print(x, y)
                y.update({"last_pos": y['pos_new'],
                          "pos_new": pisado(x, dict_persons, last_position=y['pos_new'])})
        prob_born = random.choices([0, 1], [1 - born_rate, born_rate])[0]
        prob_death = random.choices([0, 1], [1 - death_rate, death_rate])[0]
        if prob_born == 1:
            try:
                borned = born(list_persons, dict_persons)
                list_persons = borned[0]
                dict_persons = borned[1]
            except Exception as e:
                print(e, 'all dead')
                pass
            print('born', len(dict_persons))
        if prob_death == 1:
            try:
                deaths = death(list_persons, dict_persons)
                list_persons = deaths[0]
                dict_persons = deaths[1]
            except Exception as e:
                print(e, 'all dead')
                break
            print('death', len(dict_persons))

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
