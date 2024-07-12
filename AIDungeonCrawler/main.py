#! python 3
import pygame, random, nydentest2, musicTesting as mt, PIL, imagegen, time, sys
from openai import OpenAI
global floor
client = OpenAI(
    api_key = "sk-proj-PGorgZ2KBR9sN6qYqCiKT3BlbkFJ9xf8PYc7MWvBio7XlaWF"
)
enemies = []

# Sound Files Here
menu = pygame.mixer.Sound('Sound Files\\MenuSound.wav')
backMusic = 'Sound Files\\backMusic(Temp).mp3'
battleMusic = 'Sound Files\\BattleTheme.wav'
gameOver = pygame.mixer.Sound('Sound Files\\gameOver.mp3')
spellSFX = 'swordSlash.mp3'
swordSlash = 'spellSFX.mp3'
winSFX = 'winSFX.mp3'

mt.musicPlay(backMusic)
pygame.mixer.music.set_volume(.4)



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
        self.spellbook = []
        self.maxMana = 100


class Enemy:
    def __init__(self, health, name, inventoryLoot, damage,x,y ,description):
        self.health = health
        self.name = name
        self.inventoryLoot = []
        self.x = y
        self.y = x
        self.icon = (str(x) + ","+str(y))
        self.color = (250,0,0)
        self.damage = damage
        self.description = description
        self.status = "none"
#         use these for reference:
#         populateEnemy()
#         enemyAi()

class Spell:
    def __init__(self,name,manaCost,damage,statusEffect,healing):
        self.statusEffect = statusEffect
        self.name = name
        self.damage = damage
        self.manaCost = manaCost
        self.healing = healing

class Item:
    def __init__(self, typeNumber, lootTier):
        self.name = ""
        self.type = typeList[typeNumber]
        self.strength = 1
        self.element = "none"
        self.baseDamage = 1

        if lootTier == 1:
            self.strength = random.randint(1,5)
        elif lootTier == 2:
            self.strength = random.randint(4,9)
        elif lootTier == 3:
            self.strength = random.randint(8,13)
        elif lootTier == 4:
            self.strength = random.randint(12,17)
        else:
            self.strength = 1

        if typeNumber == 10:
            self.baseDamage = 5
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

            elementsList = ["","Ember ","Tidal ","Fissure ","Whirlwind ","Void "]

            if lootTier == 1:
                element = elementsList[0]
            elif lootTier >= 2 and lootTier < 4:
                element = elementsList[random.randint(1,4)]
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

#def mapEnemyAI(enemy, map):
 #   choice = random.randint(0,1)
  #  rndmNum = random.randint(-1,1)
#
 #   if choice == 0:
  #      if map[enemy.x + rndmNum][enemy.y] == 'c':
   #         map[enemy.x][enemy.y] = 'c'
    #        enemy.x += rndmNum
#
 #   else:
  #      if map[enemy.x][enemy.y + rndmNum] == 'c':
   #         map[enemy.x][enemy.y] = 'c'
    #        enemy.y += rndmNum

def prettyness(lol):
    system_data = [
        {"role": "system",
         "content": "An adventurer is fighting an enemy. Write a description for an attack when prompted with the enemy name and description, the weapon used, and the damgage dealt."},
        {"role": "user", "content": lol}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=system_data
    )

    assistant_response = response.choices[0].message.content
    system_data.append({"role": "assistant", "content": assistant_response})
    print(assistant_response)
def combat(bumpedIntoEnemy, enemyValue):
    hasfought = False
    dukingItOut = True
    print("You have entered combat.")
    pygame.mixer_music.stop()
    mt.musicPlay(battleMusic)
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
                print(str(i + 1) + ". " + theOG.inventory[i].name)
            theSubChoice = 0
            while theSubChoice not in [1,2,3,4,5,6,7,8,9,10]:
                B = input("Choose a number or choose x to go back: ").capitalize().strip()

                if B in ["",",","X"]:
                    break
                elif int(B) not in [1,2,3,4,5,6,7,8,9,10] and B != "X":
                    print("Not a valid selection, try again.")
                else:
                    hasfought = True
                    bumpedIntoEnemy.health -= theOG.inventory[theSubChoice-1].damage
                    #print("You attack with your "+theOG.inventory[theSubChoice-1].name+" dealing "+str(theOG.inventory[theSubChoice-1].damage)+" damage!")
                    print(prettyness('The hero strikes the' +bumpedIntoEnemy.name+ ' '+bumpedIntoEnemy.description+ 'with '+theOG.inventory[theSubChoice-1].name+" dealing "+str(theOG.inventory[theSubChoice-1].damage)))
                    mt.soundPlay(swordSlash)
                    if bumpedIntoEnemy.health <= 0:
                        dukingItOut = False

                        map[bumpedIntoEnemy.y][bumpedIntoEnemy.x] = 'c'
                        enemies.pop(enemyValue) #enemyValue is enemy list number
                        #print(f"enemy {enemyValue} should be killed")
                        #print(enemyValue)
                        #Map Enemie Picture Location Pop goes here

                        break

        elif theChoice == "S":
            for i in range(len(theOG.spellbook)):
                print(str(i + 1) + ". " + theOG.spellbook[i].name + "," + str(theOG.spellbook[i].manaCost) + " mana")
            theSubChoice = 0
            while theSubChoice not in [1,2,3,4,5,6]:
                B = input("Choose a number or choose x to go back: ").capitalize().strip()
                theSubChoice = int(B)
                if theSubChoice not in [1,2,3,4,5,6] and B != "X":
                    print("Not a valid selection, try again.")
                elif B in ["",",","X"]:
                    break
                elif theOG.mana < theOG.spellbook[theSubChoice-1].manaCost:
                    print("Not enough mana, try again.")
                else:
                    hasfought = True
                    theOG.mana -= theOG.spellbook[theSubChoice-1].manaCost
                    bumpedIntoEnemy.health -= theOG.spellbook[theSubChoice-1].damage
                    print("You cast "+theOG.spellbook[theSubChoice-1].name+".")
                    mt.soundPlay(spellSFX)
                    print("The " + bumpedIntoEnemy.name + " takes " + str(theOG.spellbook[theSubChoice-1].damage) + "damage.")
                    if theOG.spellbook[theSubChoice-1].statusEffect != "none":
                        print("The " + bumpedIntoEnemy.name + " is now " + str(theOG.spellbook[theSubChoice-1].statusEffect) + ".")
                    if theOG.spellbook[theSubChoice-1].healing > 0:
                        theOG.health += theOG.spellbook[theSubChoice-1].healing
                        print("Your health has increased by " + theOG.spellbook[theSubChoice-1].healing + "points")
                    if theOG.health <= 0:
                        dukingItOut = False
                        break
                    if bumpedIntoEnemy.health <= 0:
                        dukingItOut = False

                        map[bumpedIntoEnemy.y][bumpedIntoEnemy.x] = 'c'
                        enemies.pop(enemyValue) #enemyValue is enemy list number
                        #print(f"enemy {enemyValue} should be killed")
                        #print(enemyValue)
                        #Map Enemie Picture Location Pop goes here

                        break
                    break

        if hasfought and dukingItOut:
            theOG.health -= bumpedIntoEnemy.damage
            print("The " +bumpedIntoEnemy.name+ " hits you for " + str(bumpedIntoEnemy.damage) + " damage!")
            # monster fights back
            if theOG.health <= 0:
                dukingItOut = False
                break
            if bumpedIntoEnemy.health <= 0:
                dukingItOut = False
                break
        else:
            break
    if not dukingItOut:
        theOG.mana = theOG.maxMana#right here
        pygame.mixer_music.stop()
        if theOG.health < 1:
            mt.soundPlay(gameOver)
        else:
            print('You Won the Battle! \n+1 Swags Given!')
            mt.musicPlay(backMusic)



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
    if "\n\n" in l:
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
        print(final)
        if len(final) < 4:
            print("fixed bc Xavier is a genius")
            return aienemygen(lol)
        return final
    else:
        print("fixed bc Xavier is a genius")
        return aienemygen(lol)




def gencheck(x,y):
    while map[x][y] != "c":
        x = random.randint(2,MAP_WIDTH-2)
        y = random.randint(2,MAP_HEIGHT-2)
    map[x][y] = 'E'
    return [x,y]
def populateEnemy(monsterTier):
    aiimport = aienemygen('tiny enemy')
    name = aiimport[0]
    speed = aiimport[1]
    armor = aiimport[2]
    description = aiimport[3]
    x = random.randint (2,MAP_WIDTH-2)
    y = random.randint (2,MAP_HEIGHT-2)



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
    for i in range(10):
        x = random.randint(2, MAP_WIDTH-2)
        y = random.randint(2, MAP_HEIGHT-2)
        k = gencheck(x, y)
        enemies.append(Enemy(health, name, inventoryLoot, damage,k[0],k[1],description))
    aiimport = aienemygen('Fat enemy')
    name = aiimport[0]
    speed = aiimport[1]
    armor = aiimport[2]
    try:
        description = aiimport[3]
    except IndexError:
        print("IndexError aiimport[3]")
    x= random.randint (2,RECT_WIDTH-2)
    y= random.randint (2,RECT_HEIGHT-2)



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
            try:
                inventoryLoot.append(Item(random.randint(0,2),random.randint(1,4)))
            except:
                print("error in inventoryLoot.append")

    # typeNumber 0-2, lootTier 1-4
    for i in range (10):
        k = gencheck(x, y)
        enemies.append(Enemy(health, name, inventoryLoot, damage,k[0],k[1],description))
    aiimport = aienemygen('quick enemy')

    name = aiimport[0]
    speed = aiimport[1]
    armor = aiimport[2]
    description = aiimport[3]
    x= random.randint (2,RECT_WIDTH-2)
    y= random.randint (2,RECT_HEIGHT-2)



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
    print(enemies[0].name)
    print(map)


letterList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


def mapgen(height, width):
    global map
    map = makemaze(height, width)

    populateEnemy(1)


def lootgen():
    print("lootgen")

print(map)



print("Hello World") #this is a placeholder to mark the start of our program

letterList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

gap = 1
sqWidth = 30

#width = 40
#height = 40

dukingItOut = False

typeList = ["sword","dagger","magicStaff","","","","","","","","",""]

placeholder = 2
placeholder2 = 1
item0 = Item(placeholder,placeholder2)
item1 = Item(placeholder,placeholder2)
item2 = Item(placeholder,placeholder2)
item3 = Item(placeholder,placeholder2)
item4 = Item(placeholder,placeholder2)
item5 = Item(placeholder,placeholder2)
item6 = Item(placeholder,placeholder2)
item7 = Item(placeholder,placeholder2)
item8 = Item(placeholder,placeholder2)
item9 = Item(placeholder,placeholder2)

theOG = Player()

# theOG.inventory.append(Item(1,1))

item0 = Item(1,1)

theOG.spellbook.append(Spell("Lesser Healing",50,0,"none", 75))
theOG.spellbook.append(Spell("Greater Healing",70,0,"none",300))
theOG.spellbook.append(Spell("Icicle",25,20,"frozen",0))
theOG.spellbook.append(Spell("Fireball",75,100,"burning",0))
theOG.spellbook.append(Spell("Lightning Strike",75,600,"none",0))
theOG.spellbook.append(Spell("Earthquake",100,1000,"none",0))

theOG.name = input("Character Name: ")

print("Hello there, general " + theOG.name + ". \nYou have been stranded in a labyrinth, and the only way is down. \nNo use in staying here.")


# Epiic gaymer fortnite poopy doopy hehe here
def check_enemy(x, y):
    for e in enemies:
        if x == e.x and y == e.y:
            return e

# ----nyden stupid code for graphics begin---- #
FRAMERATE = 120
RECT_WIDTH = 7
RECT_HEIGHT = 7
MAP_WIDTH = 50
MAP_HEIGHT = 50
WIDTH = 700
HEIGHT = 700
testing = True

mapgen(MAP_WIDTH, MAP_HEIGHT)

if testing:
    wall = pygame.image.load('wall.jpg')
    hero = pygame.image.load('hero.jpg')
    floortile = pygame.image.load('stonefloor.jpg')
    enemy = pygame.image.load('dragon.jpg')
else:
    hero = imagegen.generate("Create an image of a peanut man knight hero")
    wall = imagegen.generate("Create an image of a brick wall texture")
    floortile = imagegen.generate("Create an image of a stone floor texture")
    enemy = imagegen.generate("Create an image of a fearsom dragon")
wall_img = pygame.transform.scale(wall, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
hero_img = pygame.transform.scale(hero, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
floor_img = pygame.transform.scale(floortile, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
enemy_img = pygame.transform.scale(enemy, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI Dungeon Crawler')
clock = pygame.time.Clock()
running = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BLUE = (0, 0, 200)

playerX = nydentest2.find_top_empty(map)
playerY = 0
camX = RECT_WIDTH // 2
camY = RECT_HEIGHT // 2


def within_cam_range(x, y):
    sidex = RECT_WIDTH // 2
    sidey = RECT_HEIGHT // 2
    return (camX - sidex <= x <= camX + sidex) and (camY - sidey <= y <= camY + sidey)
def draw_images(arr):
    width_ratio = (WIDTH // RECT_WIDTH)
    height_ratio = (HEIGHT // RECT_HEIGHT)
    sizeX = RECT_WIDTH // 2
    sizeY = RECT_HEIGHT // 2
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            if within_cam_range(y, x):
                if arr[x][y] == 'w':
                    screen.blit(wall_img, ((y - camX + sizeX) * width_ratio, (x - camY + sizeY) * height_ratio))
                elif arr[x][y] == 'c' and not ((y == playerX) and (x == playerY)):
                    screen.blit(floor_img, ((y - camX + sizeX) * width_ratio, (x - camY + sizeY) * height_ratio))

zoomout = False

while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                if map[playerY][playerX + 1] != 'w' and not zoomout and not dukingItOut:
                    playerX += 1
                    if camX - playerX < 0:
                        camX += 1
            if event.key == pygame.K_a:
                try:
                    if map[playerY][playerX - 1] != 'w' and not zoomout and not dukingItOut:
                        playerX -= 1
                        if camX - playerX > 0:
                            camX -= 1
                except:
                    print('You Win!')
                    mt.soundPlay(winSFX)
            if event.key == pygame.K_w:
                if map[playerY - 1][playerX] != 'w' and not zoomout and not dukingItOut:
                    playerY -= 1
                    if camY - playerY > 0:
                        camY -= 1
            if event.key == pygame.K_s:
                try:
                    if map[playerY + 1][playerX] != 'w' and not zoomout and not dukingItOut:
                        playerY += 1
                        if camY - playerY < 0:
                            camY += 1
                except:
                    print('You have escaped the Dungeon!')
                    mt.soundPlay(winSFX)
                    time.sleep(4)
                    sys.exit()
            if event.key == pygame.K_e:
                if not dukingItOut:
                    zoomout = not zoomout
                    if zoomout:
                        RECT_HEIGHT = MAP_HEIGHT
                        RECT_WIDTH = MAP_WIDTH
                        camX = RECT_WIDTH // 2
                        camY = RECT_HEIGHT // 2
                        wall_img = pygame.transform.scale(wall, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
                        hero_img = pygame.transform.scale(hero, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
                        floor_img = pygame.transform.scale(floortile, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
                        enemy_img = pygame.transform.scale(enemy, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
                    else:
                        RECT_HEIGHT = 7
                        RECT_WIDTH = 7
                        camX = playerX
                        camY = playerY
                        wall_img = pygame.transform.scale(wall, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
                        hero_img = pygame.transform.scale(hero, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
                        floor_img = pygame.transform.scale(floortile, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
                        enemy_img = pygame.transform.scale(enemy, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
            if event.key == pygame.K_q:
                for i in range(len(enemies)):
                    print(f"Enemy{i}: {enemies[i].x, enemies[i].y}")
            for i in range(len(enemies)):
             #   mapEnemyAI(enemies[i], map)
                try:
                    if enemies[i].y == playerY and enemies[i].x == playerX:
                        #print("enemy detected, ")

                        combat(enemies[i], i)
                        break
                    #print(enemies[i].x, enemies[i].y)
                    #print(playerX, playerY)
                except IndexError:
                    print("nyden is a bad programmer")
                    pass



    # draw_pixels(map)
    sizeX = RECT_WIDTH // 2
    sizeY = RECT_HEIGHT // 2
    draw_images(map)
    for e in enemies:
        screen.blit(enemy_img, ((e.x - camX + sizeX) * (WIDTH // RECT_WIDTH), (e.y - camY + sizeY) * (HEIGHT // RECT_HEIGHT)))
    try:
        screen.blit(hero_img,((playerX - camX + sizeX) * (WIDTH // RECT_WIDTH), (playerY - camY + sizeY) * (HEIGHT // RECT_HEIGHT)))
    except:
        print(playerX, camX, playerY, camY)
    pygame.display.flip()
    clock.tick(FRAMERATE)

# NO SWEARING, CURSING, OR OTHER OBSCENITIES >:(
