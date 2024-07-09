#! python 3
import pygame, sys, random, time, base64, io, requests, PIL, os, numpy as np
from openai import OpenAI
from urllib.request import urlretrieve
from datetime import datetime  # for formatting date returned with images
import tkinter as tk  # for GUI thumbnails of what we got


global floor
client = OpenAI(
    api_key = "sk-proj-MfQUU6kDUqNSxpmi7q9ET3BlbkFJbM27VwUuRHqM4qi2ePKh"
)


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
def aienemygen(lol):


    system_data = [
        {"role": "system", "content": "Generate a generic dungeon crawler enemy, create a name. Then give a brief description. Then specify if the armor is Light, Medium, or Heavy after that using that wording Then say if its Quick, Average, or Slow, with that wording. "},
        {"role": "user", "content": lol}
    ]

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = system_data
    )

    assistant_response = response.choices[0].message.content
    system_data.append({"role": "assistant", "content": assistant_response})
    print(assistant_response)
    l = str(assistant_response)
    k = l.find("Description: ")
    c = 0
    name = ''
    for i in range(6,k-2):
        name = name + l[i]
    final = [name]

    match l[len(l)-1]:
        case "k":
            final.append("Quick")
            c = 5
        case'e':
            final.append("Average")
            c = 7
        case 'w':
            final.append("Slow")
            c = 4

    match l[len(l)-1-c-9]:

        case 'y':
            final.append("Heavy")
            c += 5
        case 'm':
            final.append("Medium")
            c = c + 6
        case 't':
            final.append("Light")
            c = c + 5

    description = ''
    for i in range(k, (len(l)-c-17)):
        description = description + l[i]

    final.append(description)
    return final

def gencheck(x,y):
    if map[x][y] == "c":
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
    global map
    height = 10
    width = 10
    map = makemaze(height, width)


print ( map)



print("Hello World") #this is a placeholder to mark the start of our program

letterList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

gap = 1
sqWidth = 30
width = mapgen().width
height = mapgen().height
surface = pygame.display.set_mode((width,height))

typeList = ["sword","dagger","magicStaff"]




# NO SWEARING, CURSING, OR OTHER OBSCENITIES >:(

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

#! python 3
# Sprite Implementation for the AI Dungeon Crawler, Currently Non-functional


class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

pygame.sprite.Group(enemies)
pygame.sprite.Group(hero)
pygame.sprite.Group.add(enemies)
pygame.sprite.Group.add(hero)


def add_internal(self, sprite):
    pygame.sprite.Group.add_internal(self, sprite)

def remove_internal(self, sprite):
    pygame.sprite.Group.remove_internal(self, sprite)



    def old_package(version, minimum):  # Block old openai python libraries before today's
        version_parts = list(map(int, version.split(".")))
        minimum_parts = list(map(int, minimum.split(".")))
        return version_parts < minimum_parts

    if old_package(openai.__version__, "1.2.3"):
        raise ValueError(f"Error: OpenAI version {openai.__version__}"
                         " is less than the minimum version 1.2.3\n\n"
                         ">>You should run 'pip install --upgrade openai')")


    # client = OpenAI(api_key="sk-xxxxx")  # don't do this, OK?
    client = OpenAI()  # will use environment variable "OPENAI_API_KEY"

    prompt = (
        "Subject: ballet dancers posing on a beam. "  # use the space at end
        "Style: romantic impressionist painting."  # this is implicit line continuation
    )

    image_params = {
        "model": "dall-e-2",  # Defaults to dall-e-2
        "n": 1,  # Between 2 and 10 is only for DALL-E 2
        "size": "1024x1024",  # 256x256, 512x512 only for DALL-E 2 - not much cheaper
        "prompt": prompt,  # DALL-E 3: max 4000 characters, DALL-E 2: max 1000
        "user": "myName",  # pass a customer ID to OpenAI for abuse monitoring
    }

    ## -- You can uncomment the lines below to include these non-default parameters --

    image_params.update({"response_format": "b64_json"})  # defaults to "url" for separate download

    ## -- DALL-E 3 exclusive parameters --
    # image_params.update({"model": "dall-e-3"})  # Upgrade the model name to dall-e-3
    # image_params.update({"size": "1792x1024"})  # 1792x1024 or 1024x1792 available for DALL-E 3
    # image_params.update({"quality": "hd"})      # quality at 2x the price, defaults to "standard"
    # image_params.update({"style": "natural"})   # defaults to "vivid"

    # ---- START
    # here's the actual request to API and lots of error catching
    try:
        images_response = client.images.generate(**image_params)
    except openai.APIConnectionError as e:
        print("Server connection error: {e.__cause__}")  # from httpx.
        raise
    except openai.RateLimitError as e:
        print(f"OpenAI RATE LIMIT error {e.status_code}: (e.response)")
        raise
    except openai.APIStatusError as e:
        print(f"OpenAI STATUS error {e.status_code}: (e.response)")
        raise
    except openai.BadRequestError as e:
        print(f"OpenAI BAD REQUEST error {e.status_code}: (e.response)")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

    # make a file name prefix from date-time of response
    images_dt = datetime.utcfromtimestamp(images_response.created)
    img_filename = images_dt.strftime('DALLE-%Y%m%d_%H%M%S')  # like 'DALLE-20231111_144356'

    # get the prompt used if rewritten by dall-e-3, null if unchanged by AI
    revised_prompt = images_response.data[0].revised_prompt

    # get out all the images in API return, whether url or base64
    # note the use of pydantic "model.data" style reference and its model_dump() method
    image_url_list = []
    image_data_list = []
    for image in images_response.data:
        image_url_list.append(image.model_dump()["url"])
        image_data_list.append(image.model_dump()["b64_json"])

    # Initialize an empty list to store the Image objects
    image_objects = []

    # Check whether lists contain urls that must be downloaded or b64_json images
    if image_url_list and all(image_url_list):
        # Download images from the urls
        for i, url in enumerate(image_url_list):
            while True:
                try:
                    print(f"getting URL: {url}")
                    response = requests.get(url)
                    response.raise_for_status()  # Raises stored HTTPError, if one occurred.
                except requests.HTTPError as e:
                    print(f"Failed to download image from {url}. Error: {e.response.status_code}")
                    retry = input("Retry? (y/n): ")  # ask script user if image url is bad
                    if retry.lower() in ["n", "no"]:  # could wait a bit if not ready
                        raise
                    else:
                        continue
                break
            image_objects.append(Image.open(BytesIO(response.content)))  # Append the Image object to the list
            image_objects[i].save(f"{img_filename}_{i}.png")
            print(f"{img_filename}_{i}.png was saved")
    elif image_data_list and all(image_data_list):  # if there is b64 data
        # Convert "b64_json" data to png file
        for i, data in enumerate(image_data_list):
            image_objects.append(Image.open(BytesIO(base64.b64decode(data))))  # Append the Image object to the list
            image_objects[i].save(f"{img_filename}_{i}.png")
            print(f"{img_filename}_{i}.png was saved")
    else:
        print("No image data was obtained. Maybe bad code?")

    ## -- extra fun: pop up some thumbnails in your GUI if you want to see what was saved

    if image_objects:
        # Create a new window for each image
        for i, img in enumerate(image_objects):
            # Resize image if necessary
            if img.width > 512 or img.height > 512:
                img.thumbnail((512, 512))  # Resize while keeping aspect ratio

            # Create a new tkinter window
            window = tk.Tk()
            window.title(f"Image {i}")

            # Convert PIL Image object to PhotoImage object
            tk_image = ImageTk.PhotoImage(img)

            # Create a label and add the image to it
            label = tk.Label(window, image=tk_image)
            label.pack()

            # Run the tkinter main loop - this will block the script until images are closed
            window.mainloop()

            from openai import OpenAI
            import textwrap
            client = OpenAI(
                api_key="sk-proj-MfQUU6kDUqNSxpmi7q9ET3BlbkFJbM27VwUuRHqM4qi2ePKh"

            )

            def enemygen(lol):

                system_data = [
                    {"role": "system",
                     "content": "Generate a generic dungeon crawler enemy, create a name. Then give a brief description. Then specify if the armor is Light, Medium, or Heavy after that using that wording Then say if its Quick, Average, or Slow, with that wording. "},
                    {"role": "user", "content": lol}
                ]

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=system_data
                )

                assistant_response = response.choices[0].message.content
                system_data.append({"role": "assistant", "content": assistant_response})
                print('\n'.join(textwrap.wrap(assistant_response, 75)))
                return assistant_response

            l = str(enemygen(""))
            k = l.find("Description: ")
            c = 0
            name = ''
            for i in range(6, k):
                name = name + l[i]
            print(name)

            match l[len(l) - 1]:
                case "k":
                    print("Quick")
                    c = 5
                case 'e':
                    print("Average")
                    c = 7
                case 'w':
                    print("Slow")
                    c = 4

            match l[len(l) - 1 - c - 9]:

                case 'y':
                    print("Heavy")
                    c += 5
                case 'm':
                    print("Medium")
                    c = c + 6
                case 't':
                    print("Light")
                    c = c + 5

            description = ''
            for i in range(k, (len(l) - c - 17)):
                description = description + l[i]

            print(description)


client = OpenAI(api_key = "sk-proj-MduORQWiwbEHFJDHNQnLT3BlbkFJzXOJKG2q6utiMNOtx3ID")

response = client.images.generate(
  model = "dall-e-3",
  prompt = "90's grid based dungeon crawler enemy sprite",
  size = "1024x1024",
  quality = "standard",
  n=1,
)

image_url = response.data[0].url
urlretrieve(image_url, "image.png") #specify path
print(image_url)

response = requests.get(image_url)
img = Image.open(io.BytesIO(response.content))

img.show()

class Enemy(pygame.sprite.Sprite):
