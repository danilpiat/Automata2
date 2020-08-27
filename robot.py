import numpy as np
import pandas as pd
from termcolor import colored, cprint

class Robot:
    def __init__(self, s=None, sep=None, header=None, durability=None):
        self.y = None
        self.x = None
        self.shape_x = None
        self.shape_y = None
        self.map = None
        self.__load_map(s, sep, header)
        if durability==None:
            self.drill_durability = 50
        else:
            self.drill_durability = durability
        self.bind = None
        self.counter = 1000
        self.direct_variants = ['up', 'left', 'down', 'right']
        self.direct = self.direct_variants[self.counter % 4]
        self.exit_found = False

    def __load_map(self, s=None, sep=None, header=None):
        if s is None:
            s = "tests/map_simple"
        if sep is None:
            sep = ";"
        self.map = pd.read_csv(s, sep=sep, header=header).astype(str)
        self.shape_y = self.map.shape[0]
        self.shape_x = self.map.shape[1]
        self.y = self.shape_y//2
        self.x = self.shape_x//2
        print(self.map.values)
        se = set()
        for i in self.map.values:
            se.update(set(i))
        if se != set(['0', '1', 'e']):
            raise Exception("")
        self.check_exit()

    def rotate_right(self):
        self.counter += 1
        self.direct = self.direct_variants[self.counter % 4]

    def rotate_left(self):
        if self.counter==0:
           self.counter = 1000
        self.counter -= 1
        self.direct = self.direct_variants[self.counter % 4]

    def action(self, node):
     if node.op == "print_map":
        self.print_map()
     if self.exit_found != True:
        if node.op == "forward" or node.op == "up":
            return self.forward()
        elif node.op == "back" or node.op == "down":
            return self.back()
        elif node.op == "left":
            return self.left()
        elif node.op == "right":
            return self.right()
        elif node.op == "rotate_left":
            self.rotate_left()
            return True
        elif node.op == "rotate_right":
            self.rotate_right()
            return True
        elif node.op == "measure":
            return self.measure()
        elif node.op == "demolish":
            return self.demolish()
        self.check_exit()

    def check(self, x, y):
        if self.map[x][y] == '0':
            return True
        elif self.map[x][y] == '1':
            return False
        elif self.map[x][y] == 'e':
            print("exit")
            return True

    def forward(self):
        if self.direct == 'up':
            return self.__up()
        elif self.direct == 'left':
            return self.__left()
        elif self.direct == 'down':
            return self.__down()
        elif self.direct == 'right':
            return self.__right()

    def back(self):
        if self.direct == 'down':
            return self.__up()
        elif self.direct == 'right':
            return self.__left()
        elif self.direct == 'up':
            return self.__down()
        elif self.direct == 'left':
            return self.__right()

    def right(self):
        if self.direct == 'left':
            return self.__down()
        elif self.direct == 'down':
            return self.__right()
        elif self.direct == 'right':
            return self.__up()
        elif self.direct == 'up':
            return self.__left()

    def left(self):
        if self.direct == 'right':
            return self.__down()
        elif self.direct == 'up':
            return self.__right()
        elif self.direct == 'left':
            return self.__up()
        elif self.direct == 'down':
            return self.__left()

    def __up(self):
        if (self.y - 1) >= 0:
            if self.check(self.x, self.y-1):
                self.y -= 1
                return True
        return False

    def __down(self):
        if (self.y + 1) < self.shape_y:
            if self.check(self.x, self.y+1):
               self.y += 1
               return True
        return False

    def __left(self):
        if (self.x + 1) < self.shape_x:
            if self.check(self.x+1, self.y):
               self.x += 1
               return True
        return False

    def __right(self):
        if (self.x - 1) >= 0:
            if self.check(self.x-1, self.y):
               self.x -= 1
               return True
        return False

    def print_map(self):
        t = self.map.copy()
        t[self.x][self.y] = 'X'
        print("-" * self.shape_x * 5)
        print("durabilty:%s" %(self.drill_durability))
        print(t)
        print("-" * self.shape_x * 5)

    def measure(self):
        if self.direct == 'up':
            if (self.y - 1) >= 0:
                return self.map[self.x][self.y - 1]
            else:
                return 'o'
        elif self.direct == 'left':
            if (self.x + 1) < self.shape_x:
                return self.map[self.x+1][self.y]
            else:
                return 'o'
        elif self.direct == 'down':
            if (self.y + 1) < self.shape_y:
                return self.map[self.x][self.y+1]
            else:
                return 'o'
        elif self.direct == 'right':
            if (self.x - 1) >= 0:
                return self.map[self.x-1][self.y]
            else:
                return 'o'


    def demolish(self):
        if (self.y - 1) >= 0:
            if self.map[self.x][(self.y - 1)] == '1':
                self.drill_durability -= 1
                self.map[self.x][(self.y - 1)] = '0'
                return True
            else:
                return False
        else:
            return False

    def demolish(self):
        if self.direct == 'up':
            if (self.y - 1) >= 0:
                if self.map[self.x][self.y - 1] == '1':
                    self.drill_durability -= 1
                    self.map[self.x][self.y - 1] = '0'
                    return True
                else:
                    return False
            else:
                return False
        elif self.direct == 'left':
            if (self.x + 1) < self.shape_x:
                if self.map[self.x+1][self.y] == '1':
                    self.drill_durability -= 1
                    self.map[self.x+1][self.y] = '0'
                    return True
                else:
                    return False
            else:
                return False
        elif self.direct == 'down':
            if (self.y + 1) < self.shape_y:
                if self.map[self.x][self.y+1] == '1':
                    self.drill_durability -= 1
                    self.map[self.x][self.y + 1] = '0'
                    return True
                else:
                    return False
            else:
                return False
        elif self.direct == 'right':
            if (self.x - 1) >= 0:
                if self.map[self.x-1][self.y] == '1':
                    self.drill_durability -= 1
                    self.map[self.x-1][self.y] = '0'
                    return True
                else:
                    return False
            else:
                return False

    def check_exit(self):
        if self.map[self.x][self.y] == 'e':
            self.exit_found = True




"""

    def rotate_left(self):
        z = pd.DataFrame(self.map.transpose().copy())
        for i in range(self.shape_y):
            for j in range(self.shape_x):
                z.iloc[j, self.shape_x - i - 1] = self.map.iloc[i,j]
        t = self.x
        self.x = self.shape_y-self.y-1
        self.y = t
        self.map = z

    def rotate_right(self):
        z = pd.DataFrame(self.map.transpose().copy())
        for i in range(self.shape_y):
            for j in range(self.shape_x):
                z.iloc[self.shape_y - j - 1, i] = self.map.iloc[i,j]
        t = self.x
        self.x = self.y
        self.y = t
        self.map = z


"""