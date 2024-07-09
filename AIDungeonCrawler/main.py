#! python 3
import pygame, sys, random, time, numpy as np, musicTesting as mt
from openai import OpenAI
global floor
client = OpenAI(
    api_key = "sk-proj-MfQUU6kDUqNSxpmi7q9ET3BlbkFJbM27VwUuRHqM4qi2ePKh"
)
enemies = []

floor = 1
class Player:
    def __init__(self):
        #Health and mana are not needed for the player's initial input as they can be amended later on
        self.mana = 100
        self.health = 100
        self.inventory = [item0,item1,item2,item3,item4,item5,item6,item7,item8,item9]
        #inventory will be kept to a max of 10, however, empty spaces are not condoned
        self.x = 0
        self.y = 0
        self.icon = "@"
        self.color = (0,250,0)
        self.gold = 0
        self.mana = 100
        self.name = ""


class Enemy:
    def __init__(self, health, name, inventoryLoot, damage,x,y ,description):
        self.health = health
        self.name = name
        self.inventoryLoot = []
        self.x = x
        self.y = y
        self.icon = (str(x) + ","+str(y))
        self.color = (250,0,0)
        self.damage = damage
        self.description = description
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

        if typeNumber == 999:
            self.baseDamage = 0
            self.name = "placeholderItem"
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

#def mapEnemyAI():

    #isn't this term used elsewhere?

def combat(bumpedIntoEnemy):
    dukingItOut = True
    print("You have entered combat.")
    while dukingItOut:
        print(f"""
    {theOG.name}                     {bumpedIntoEnemy.name}
    Health: {theOG.health} Health: {bumpedIntoEnemy.health}
    Mana: {theOG.mana}
    
    Choose your weapon: 
    I for inventory
    S for spells
    """)
        theChoice = input().capitalize().strip()
        if theChoice == "I":
            for i in range(len(theOG.inventory)):
                print((i+1) + ". " + theOG.inventory[i].name)
            theSubChoice = int(input("Choose your number: "))
            print("You attack with your "+theOG.inventory[theSubChoice-1].name+" dealing "+theOG.inventory[theSubChoice-1].damage+" damage!")
        elif theChoice == "S":
            for i in range(len(theOG.spellbook)):
                print((i + 1) + ". " + theOG.inventory[i].name)
            theSubChoice = int(input("Choose your number: "))
            print("You cast "++"")
        else:
            dukingItOut = True

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
    while map[x][y] != "c":
        x = random.randint(0,RECT_WIDTH-1)
        y = random.randint(0,RECT_HEIGHT-1)
    map[x][y] = 'E'
    return [x,y]
def populateEnemy(monsterTier):
    aiimport = aienemygen('tiny enemy')
    name = aiimport[0]
    speed = aiimport[1]
    armor = aiimport[2]
    description = aiimport[3]
    x= random.randint (0,RECT_WIDTH)
    y= random.randint (0,RECT_HEIGHT)



    match armor:
        case 'Light':
            health = random.randint(30*monsterTier,50*monsterTier)
        case 'Medium':
            health = random.randint(50*monsterTier,70*monsterTier)
        case 'Heavy':
            health = random.randint(70*monsterTier,100*monsterTier)
    match speed:
        case 'Slow':
            damage = random.randint(3*monsterTier,5*monsterTier)
        case 'Average':
            damage = random.randint(5*monsterTier,7*monsterTier)
        case 'Quick':
            damage = random.randint(7*monsterTier,10*monsterTier)
    inventoryLoot = []

    for x in range(monsterTier):
        if random.randint(0,2) == 2:
            inventoryLoot.append(Item(random.randint(0,2),random.randint(1,4)))

    # typeNumber 0-2, lootTier 1-4
    for i in range (10):
        k = gencheck(x, y)
        enemies.append(Enemy(health, name, inventoryLoot, damage,k[0],k[1],description))
    aiimport = aienemygen('Fat enemy')
    name = aiimport[0]
    speed = aiimport[1]
    armor = aiimport[2]
    description = aiimport[3]
    x= random.randint (0,RECT_WIDTH)
    y= random.randint (0,RECT_HEIGHT)



    match armor:
        case 'Light':
            health = random.randint(30*monsterTier,50*monsterTier)
        case 'Medium':
            health = random.randint(50*monsterTier,70*monsterTier)
        case 'Heavy':
            health = random.randint(70*monsterTier,100*monsterTier)
    match speed:
        case 'Slow':
            damage = random.randint(3*monsterTier,5*monsterTier)
        case 'Average':
            damage = random.randint(5*monsterTier,7*monsterTier)
        case 'Quick':
            damage = random.randint(7*monsterTier,10*monsterTier)
    inventoryLoot = []

    for x in range(monsterTier):
        if random.randint(0,2) == 2:
            inventoryLoot.append(Item(random.randint(0,2),random.randint(1,4)))

    # typeNumber 0-2, lootTier 1-4
    for i in range (10):
        k = gencheck(x, y)
        enemies.append(Enemy(health, name, inventoryLoot, damage,k[0],k[1],description))
    aiimport = aienemygen('quick enemy')
    name = aiimport[0]
    speed = aiimport[1]
    armor = aiimport[2]
    description = aiimport[3]
    x= random.randint (0,RECT_WIDTH)
    y= random.randint (0,RECT_HEIGHT)



    match armor:
        case 'Light':
            health = random.randint(30*monsterTier,50*monsterTier)
        case 'Medium':
            health = random.randint(50*monsterTier,70*monsterTier)
        case 'Heavy':
            health = random.randint(70*monsterTier,100*monsterTier)
    match speed:
        case 'Slow':
            damage = random.randint(3*monsterTier,5*monsterTier)
        case 'Average':
            damage = random.randint(5*monsterTier,7*monsterTier)
        case 'Quick':
            damage = random.randint(7*monsterTier,10*monsterTier)
    inventoryLoot = []

    for x in range(monsterTier):
        if random.randint(0,2) == 2:
            inventoryLoot.append(Item(random.randint(0,2),random.randint(1,4)))

    # typeNumber 0-2, lootTier 1-4
    for i in range (10):
        k = gencheck(x, y)
        enemies.append(Enemy(health, name, inventoryLoot, damage,k[0],k[1],description))
    print(enemies)
    print(enemies[2].name)


letterList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


def mapgen(height, width):
    global map
    map = makemaze(height, width)
    populateEnemy(1)


FRAMERATE = 120
RECT_WIDTH = 50
RECT_HEIGHT = 50
WIDTH = 700
HEIGHT = 700


def lootgen():
    print("lootgen")

print(map)



print("Hello World") #this is a placeholder to mark the start of our program

letterList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

gap = 1
sqWidth = 30

try:
    width = mapgen().width
    height = mapgen().height
    surface = pygame.display.set_mode((width, height))
except:
    print("Error lines 449-451")


typeList = ["sword","dagger","magicStaff"]

item0 = Item(999,0)
item1 = Item(999,0)
item2 = Item(999,0)
item3 = Item(999,0)
item4 = Item(999,0)
item5 = Item(999,0)
item6 = Item(999,0)
item7 = Item(999,0)
item8 = Item(999,0)
item9 = Item(999,0)

theOG = Player()

theOG.inventory.append(Item(1,1))
theOG.name = input("Character Name: ")

print("Hello there, general " + theOG.name + ". \nYou have been stranded in a labyrinth, and the only way is down. \nNo use in staying here.")




# NO SWEARING, CURSING, OR OTHER OBSCENITIES >:(