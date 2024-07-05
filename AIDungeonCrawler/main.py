#! python 3
import pygame, sys, random, time, numpy as np
from openai import OpenAI
global floor

floor = 1
class Player:
    def __init__(self, mana, health):
        self.mana = 100
        self.health = 100
        self.inventory = [''*10]
        self.x = 0
        self.y = 0
        self.icon = "@"
        self.color = (0,250,0)
        self.gold = 0


class Enemy:
    def __init__(self, health, name, inventoryLoot, damage, monsterPortrait):
        self.health = 1
        self.name = "Jerry"
        self.inventoryLoot = []
        self.x = width-1
        self.x = height-1
        self.icon = letterList[random.randInt(0,51)]
        self.color = (250,0,0)
        self.damage = 1
        self.monsterPortrait
#         use these for reference:
#         populateEnemy()
#         enemyAi()

class Item:
    def __init__(self, typeNumber, lootTier):
        self.name = ""
        self.type = typeList[typeNumber]
        self.strength
        self.element = "none"

        if lootTier == 1:
            self.strength = random.randInt(0,5)
        elif lootTier == 2:
            self.strength = random.randInt(4,9)
        elif lootTier == 3:
            self.strength = random.randInt(8,13)
        elif lootTier == 4:
            self.strength = random.randInt(12,17)
        else:
            self.strength = 0

        if typeList[typeNumber] == "sword":
            self.baseDamage = 40

            if self.strength >= 1:
                self.name = "Sword" + str(self.strength)
            else:
                self.name = "Sword"
        elif typeList[typeNumber] == "bow":
            self.baseDamage = 25

            if self.strength >= 1:
                self.name = "Dagger" + str(self.strength)
            else:
                self.name = "Dagger"
        elif typeList[typeNumber] == "magicStaff":
            self.baseDamage = 50

            elementsList = ["","Fireball ","Tidal ","Fissure ","Whirlwind ","Void "]

            if lootTier == 1:
                element = elementsList[0]
            elif lootTier >= 2 and lootTier < 4:
                element = elementsList[random.randInt(1,4)]
            elif lootTier == 4:
                element = elementsList[5]
            else:
                print("Error: invalid lootTier assignment")
                element = ""

            if self.strength >= 1:
                self.name = element + "Staff" + str(self.strength)
            else:
                self.name = element + "Staff"

        self.damage = round((self.baseDamage + self.strength)*(1+0.1*self.strength))

#         strength modifies attack damage of the sword, with strength 0 as a base of 100% damage, 1 as 110%, and so on




def makemaze(height, width):
    def printMaze(maze):
        for i in range(0, height):
            for j in range(0, width):
                if (maze[i][j] == 'u'):
                    print (str(maze[i][j]), end=" ")
                elif (maze[i][j] == 'c'):
                    print( str(maze[i][j]), end=" ")
                else:
                    print( str(maze[i][j]), end=" ")

            print('\n')


    # Find number of surrounding cells
    def surroundingCells(rand_wall):
        s_cells = 0
        if (maze[rand_wall[0] - 1][rand_wall[1]] == 'c'):
            s_cells += 1
        if (maze[rand_wall[0] + 1][rand_wall[1]] == 'c'):
            s_cells += 1
        if (maze[rand_wall[0]][rand_wall[1] - 1] == 'c'):
            s_cells += 1
        if (maze[rand_wall[0]][rand_wall[1] + 1] == 'c'):
            s_cells += 1

        return s_cells

    wall = 'w'
    cell = 'c'
    unvisited = 'u'
    maze = []



    # Denote all cells as unvisited
    for i in range(0, height):
        line = []
        for j in range(0, width):
            line.append(unvisited)
        maze.append(line)

    # Randomize starting point and set it a cell
    starting_height = int(random.random() * height)
    starting_width = int(random.random() * width)
    if (starting_height == 0):
        starting_height += 1
    if (starting_height == height - 1):
        starting_height -= 1
    if (starting_width == 0):
        starting_width += 1
    if (starting_width == width - 1):
        starting_width -= 1

    # Mark it as cell and add surrounding walls to the list
    maze[starting_height][starting_width] = cell
    walls = []
    walls.append([starting_height - 1, starting_width])
    walls.append([starting_height, starting_width - 1])
    walls.append([starting_height, starting_width + 1])
    walls.append([starting_height + 1, starting_width])

    # Denote walls in maze
    maze[starting_height - 1][starting_width] = 'w'
    maze[starting_height][starting_width - 1] = 'w'
    maze[starting_height][starting_width + 1] = 'w'
    maze[starting_height + 1][starting_width] = 'w'

    while (walls):
        # Pick a random wall
        rand_wall = walls[int(random.random() * len(walls)) - 1]

        # Check if it is a left wall
        if (rand_wall[1] != 0):
            if (maze[rand_wall[0]][rand_wall[1] - 1] == 'u' and maze[rand_wall[0]][rand_wall[1] + 1] == 'c'):
                # Find the number of surrounding cells
                s_cells = surroundingCells(rand_wall)

                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    # Upper cell
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0] - 1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
                        if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                    # Bottom cell
                    if (rand_wall[0] != height - 1):
                        if (maze[rand_wall[0] + 1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
                        if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] + 1, rand_wall[1]])

                    # Leftmost cell
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1] - 1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
                        if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] - 1])

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        # Check if it is an upper wall
        if (rand_wall[0] != 0):
            if (maze[rand_wall[0] - 1][rand_wall[1]] == 'u' and maze[rand_wall[0] + 1][rand_wall[1]] == 'c'):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    # Upper cell
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0] - 1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
                        if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                    # Leftmost cell
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1] - 1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
                        if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] - 1])

                    # Rightmost cell
                    if (rand_wall[1] != width - 1):
                        if (maze[rand_wall[0]][rand_wall[1] + 1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
                        if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] + 1])

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        # Check the bottom wall
        if (rand_wall[0] != height - 1):
            if (maze[rand_wall[0] + 1][rand_wall[1]] == 'u' and maze[rand_wall[0] - 1][rand_wall[1]] == 'c'):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    if (rand_wall[0] != height - 1):
                        if (maze[rand_wall[0] + 1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
                        if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] + 1, rand_wall[1]])
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1] - 1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
                        if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] - 1])
                    if (rand_wall[1] != width - 1):
                        if (maze[rand_wall[0]][rand_wall[1] + 1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
                        if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] + 1])

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        # Check the right wall
        if (rand_wall[1] != width - 1):
            if (maze[rand_wall[0]][rand_wall[1] + 1] == 'u' and maze[rand_wall[0]][rand_wall[1] - 1] == 'c'):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    if (rand_wall[1] != width - 1):
                        if (maze[rand_wall[0]][rand_wall[1] + 1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
                        if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] + 1])
                    if (rand_wall[0] != height - 1):
                        if (maze[rand_wall[0] + 1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
                        if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] + 1, rand_wall[1]])
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0] - 1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
                        if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        # Delete the wall from the list anyway
        for wall in walls:
            if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                walls.remove(wall)

    # Mark the remaining unvisited cells as walls
    for i in range(0, height):
        for j in range(0, width):
            if (maze[i][j] == 'u'):
                maze[i][j] = 'w'

    # Set entrance and exit
    for i in range(0, width):
        if (maze[1][i] == 'c'):
            maze[0][i] = 'c'
            break

    for i in range(width - 1, 0, -1):
        if (maze[height - 2][i] == 'c'):
            maze[height - 1][i] = 'c'
            break

    # Print final maze
    return maze


def gencheck(x,y):
    if maze[x][y] == "c":
        return True
    else:
        return False
def gen(height):
    i= random.randint(0,height)
    if i != 0:
        return i

def roomgen():
    print("lootgen")
#def enemyAi():

def populateEnemy(monsterTier, x, y, name, monsterPortrait):
    health = 100 + 50*monsterTier
    inventoryLoot = []

    for x in range(monsterTier):
        if random.randInt(0,2) == 2:
            inventoryLoot.append(Item(random.randInt(0,2),random.randInt(1,4)))
    Player.gold+=10
    # typeNumber 0-2, lootTier 1-4

    Enemy(health, name, inventoryLoot, monsterPortrait)
    Enemy.x = x
    Enemy.y = y

def enemygen(count,x,y):
    while count > 0:
        t = random.randint(0,x)
        r = random.randint(0,y)
        if gencheck(t,y):
            tier = floor
            populateEnemy(tier, t,y)
            count -= 1



def lootgen():
    print("lootgen")
def mapgen():
    height = 10
    width = 10
    return makemaze(height, width)


maze = mapgen()
print ( maze)



print("Hello World") #this is a placeholder to mark the start of our program

letterList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

gap = 1
sqWidth = 30
width = mapgen().width
height = mapgen().height
surface = pygame.display.set_mode((width,height))

typeList = ["sword","dagger","magicStaff"]




# NO SWEARING, CURSING, OR OTHER OBSCENITIES >:(