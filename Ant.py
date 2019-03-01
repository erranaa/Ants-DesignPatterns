from Rooms import *
from Meadow import *
import random


class Ant:
    def __init__(self, a, b):

        # determine the coordinates of anthill, origins of an ant
        self.a = a
        self.b = b
        # x, y bulunduğumuz yer
        # i, j destinasyon

    # abstractmethod

    # Handles the moving of ants

    def moveAnt(self, x, y):
        # If an ant on corner cells
        if x == 0:
            if y == 0:
                return random.choice([x+1, y+1])
                # only goes either right or down
            elif y == 19:
                return random.choice([x+1, y-1])
                # only goes either right or up
            else:
                return random.choice([x+1, y-1, y+1])
                # goes right,up or down

        elif x == 19:
            if y == 0:
                return random.choice([x-1, y+1])
                # only goes either left or down
            elif y == 19 :
                return random.choice([x-1, y-1])
                # only goes either left or up
            else:
                return random.choice([x-1, y-1, y+1])
                # goes left, up or down
        else:
            return random.choice([x-1, x+1, y-1, y+1])
            # could go 4 directions


    # RANDOM ALL THE WAY?
    # fight function, self or first ask this


class Forager(Ant):
    # find food
    def __init__(self, a, b):
        Ant.__init__(self, a, b)
        self.a = a
        self.b = b
        self.x = a
        self.y = b

        self.status = False
        self.energy = 20

        find = getattr(BuilderObject, 'grids')[a][b]
        if getattr(find, 'numAnts') != 20:
            getattr(find, 'anthill').append(Forager(a, b, a, b, a, b))
            o = getattr(find, 'numAnts')
            setattr(find, 'numAnts', o+1)

        # speciality for forager ants

    def checkStatus(self):
        if self.status:
            self.returnHome()
        else:
            self.moveAnt(self.x, self.y)

    def returnHome(self):
        x = self.x
        y = self.y
        i = self.a
        j = self.b

        if x == i and y == j:
            self.status = False
            find = getattr(BuilderObject, 'grids')[self.a][self.b]
            o = getattr(find, 'food')
            setattr(find, 'food', o+1)
            find = getattr(BuilderObject, 'grids')[self.x][self.y]
            o = getattr(find, 'food')
            setattr(find, 'food', o-1)

        if x != i or y != j:

            m = Ant.moveAnt(self, x, y)
            while x == i and y == j:
                if m != x:
                    m = Ant.moveAnt(self, m, y)
                elif m != y:
                    m = Ant.moveAnt(self, x, m)

    def fight(self):
        pass

    # return to its anthill with the found food

    def findFood(self):
        m = Ant.moveAnt(self, self.x, self.y)
        # başlangıç

        if m != self.x:
            self.x = m
            find = getattr(BuilderObject, 'grids')[self.x][self.y]
            found = getattr(find, 'food')
            if found > 0:
                self.returnHome()
                setattr(find, 'food', found-1)
                self.status = True

        elif m != self.y:
            self.y = m
            find = getattr(BuilderObject, 'grids')[self.x][self.y]
            found = getattr(find, 'food')
            if found > 0:
                self.returnHome()
                setattr(find, 'food', found-1)
                self.status = True


class Warrior(Ant):
    # fighter
    def __init__(self, a, b):
        Ant.__init__(self, a, b)
        self.a = a
        self.b = b
        self.x = a
        self.y = b

        self.strength = 100
        # warriors may have strength speciality

        find = getattr(BuilderObject, 'grids')[a][b]
        if getattr(find, 'numAnts') != 20:
            getattr(find, 'anthill').append(Warrior(a, b, a, b, a, b))
            o = getattr(find, 'numAnts')
            setattr(find, 'numAnts', o+1)

    def fight(self, second):

        # fight between a warrior ant and forager

        if type(second) is Forager:
            if second.energy < 10:
                # forager will be killed
                del second
                # WHAT HAPPENS TO THE ARRAY WHEN WE DELETE IT?
                # Once food is found, the forager must make its way back to the AntHill.
                # If it dies on it's way back, the food is lost.

            else:
                # forager will escape, but lose half of its energy
                second.energy = second.energy - 10
            return True

        # fight between 2 warrior ants
        else:
            if self.strength > second.strength:
                # first wins
                del second
                SecondChance(self)

                # SECOND CHANCE PARAMETRE OLARAK (FIRST) ALACAK

                # wrap this to first ant

                self.strength = self.strength - 4
                return True

            elif self.strength < second.strength:
                # second wins
                second.strength = second.strength - 4
                return False
            else:
                # if both have same strength
                if type(self) is SecondChance:
                    # first has second chance, first wins
                    del second
                    ants = OddsBoost(self)
                    # wrap this to first ant
                    return True
                elif type(second) is SecondChance:
                    # second has second chance, second chance
                    return False
                else:
                    # check oddsboost
                    if type(self) is OddsBoost:
                        # first has boost, first wins
                        del second
                        ants = SpeedBoost(self)
                        return True
                    else:
                        # second has boost or other probabilities, second wins or both dies
                        return False

    # if a warrior goes to another anthill and then is in it

    def control(self):
        summary = 0
        for i in range(20):
            for j in range(20):
                find = getattr(BuilderObject, 'grids')[i][j]
                if getattr(find, 'anthill'):
                    summary = summary + 1
        if summary <= 1:
            exit(0)

    def occupation(self):

        if self.strength > 0:
            # in destroying each room, ant will lose 25 points
            # so it may destroy at most 4 room
            self.strength = self.strength - 25
            # ANTHILL ROOM SAYISI CHECK
            # ANTHILL DESTROY EDILINCE YUKARDAKI CONTROL FONKSIYONUNU CAGIR
            return True
        else:
            return False

# These 3 below are built by Decorator Pattern. If a warrior wins a fight, these specialities
# below will be added to winner ant.


class SpeedBoost(Warrior):
    def __init__(self, speed):
        Warrior. __init__(self, self.a, self.b)

        self._speed = speed

    def createAnt(self):
        return self._speed.createAnt()


class SecondChance(Warrior):
    def __init__(self, chance):
        Warrior. __init__(self, self.a, self.b)

        self._chance = chance

    def createAnt(self):
        return self._chance.createAnt()


class OddsBoost(Warrior):
    def __init__(self, boost):
        Warrior. __init__(self, self.a, self.b)
        self._boost = boost

    def createAnt(self):
        return self._boost.createAnt()


class Worker(Ant):  #build rooms
    def __init__(self, a, b):
        Ant.__init__(self, a, b)
        self.a = a
        self.b = b
        self.createRoom()

        find = getattr(BuilderObject, 'grids')[a][b]
        if getattr(find, 'numAnts') != 20:
            getattr(find, 'anthill').append(Worker(a, b))
            o = getattr(find, 'numAnts')
            setattr(find, 'numAnts', o+1)

    def createRoom(self):
        a = self.a
        b = self.b
        find = getattr(BuilderObject, 'grids')[a][b]
        if getattr(find, 'food') >= 1:
            getattr(find, 'ants').remove(Worker(a, b))
            a = getattr(find, 'food')
            setattr(find, 'food', a-1)
            i = random.randint(1, 3)
            if i == 1:
                WorkerRoom(a, b)
            elif i == 2:
                ForagerRoom(a, b)
            else:
                WarriorRoom(a, b)


class QueenAnt(Ant):
    def __init__(self, a, b):
        Ant.__init__(self, a, b)
        self.a = a
        self.b = b

    def createAnthill(self, a, b):
        return Anthill(a, b)

