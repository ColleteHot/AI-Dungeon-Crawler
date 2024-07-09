import pygame
import random
import copy
import imagegen

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


def initialize_array(xsize, ysize):
    copy_array = [[False] * xsize]
    new_array = []
    for i in range(ysize):
        new_array += copy.deepcopy(copy_array)
    return new_array


def mapgen(height, width):
    global map
    map = makemaze(height, width)


FRAMERATE = 120
RECT_WIDTH = 7
RECT_HEIGHT = 7
MAP_WIDTH = 50
MAP_HEIGHT = 50
WIDTH = 700
HEIGHT = 700

mapgen(MAP_WIDTH, MAP_HEIGHT)

wall = pygame.image.load('wall.jpg')
hero = pygame.image.load('hero.jpg')
floor = pygame.image.load('stonefloor.jpg')
#hero_img = imagegen.generate("Create an image of a knight hero with a sword and shield")
#wall_img = imagegen.generate("Create an image of a brick wall texture")
#floor_img = imagegen.generate("Create an image of a stone floor texture")
wall_img = pygame.transform.scale(wall, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
hero_img = pygame.transform.scale(hero, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
floor_img = pygame.transform.scale(floor, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI Dungeon Crawler')
clock = pygame.time.Clock()
running = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BLUE = (0, 0, 200)

def find_top_empty(arr):
    for x in range(len(arr)):
        if arr[0][x] == 'c':
            return x


playerX = find_top_empty(map)
playerY = 0
camX = RECT_WIDTH // 2
camY = RECT_HEIGHT // 2

def move_camera(arr):
    sidex = RECT_WIDTH // 2
    sidey = RECT_HEIGHT // 2
    if playerX + sidex < MAP_WIDTH and playerX - sidex > 0 and playerX + sidey < MAP_HEIGHT and playerY - sidey > 0:
        return False
    else:
        return True


def within_cam_range(x, y):
    sidex = RECT_WIDTH // 2
    sidey = RECT_HEIGHT // 2
    return (camX - sidex <= x <= camX + sidex) and (camY - sidey <= y <= camY + sidey)

def draw_pixels(arr):
    width_ratio = (WIDTH // RECT_WIDTH)
    height_ratio = (HEIGHT // RECT_HEIGHT)
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            if (y == playerX) and (x == playerY):
                pygame.draw.rect(screen, BLUE, pygame.Rect(y * width_ratio, x * height_ratio,
                                                            width_ratio, height_ratio ))
            elif arr[x][y] == 'c':
                pygame.draw.rect(screen, BLACK, pygame.Rect(y * width_ratio, x * height_ratio,
                                                            width_ratio, height_ratio))
            else:
                pygame.draw.rect(screen, WHITE, pygame.Rect(y * width_ratio, x * height_ratio,
                                                            width_ratio, height_ratio))

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
                if map[playerY][playerX + 1] == 'c' and not zoomout:
                    playerX += 1
                    if camX - playerX < 0:
                        camX += 1
            if event.key == pygame.K_a:
                if map[playerY][playerX - 1] == 'c' and not zoomout:
                    playerX -= 1
                    if camX - playerX > 0:
                        camX -= 1
            if event.key == pygame.K_w:
                if map[playerY - 1][playerX] == 'c' and not zoomout:
                    playerY -= 1
                    if camY - playerY > 0:
                        camY -= 1
            if event.key == pygame.K_s:
                if map[playerY + 1][playerX] == 'c' and not zoomout:
                    playerY += 1
                    if camY - playerY < 0:
                        camY += 1
            if event.key == pygame.K_e:
                zoomout = not zoomout
                if zoomout:
                    RECT_HEIGHT = MAP_HEIGHT
                    RECT_WIDTH = MAP_WIDTH
                    camX = RECT_WIDTH // 2
                    camY = RECT_HEIGHT // 2
                    wall_img = pygame.transform.scale(wall, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
                    hero_img = pygame.transform.scale(hero, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
                    floor_img = pygame.transform.scale(floor, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
                else:
                    RECT_HEIGHT = 7
                    RECT_WIDTH = 7
                    camX = playerX
                    camY = playerY
                    wall_img = pygame.transform.scale(wall, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
                    hero_img = pygame.transform.scale(hero, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
                    floor_img = pygame.transform.scale(floor, (WIDTH // RECT_WIDTH, HEIGHT // RECT_HEIGHT))
    #draw_pixels(map)
    sizeX = RECT_WIDTH // 2
    sizeY = RECT_HEIGHT // 2
    draw_images(map)
    screen.blit(hero_img, ((playerX - camX + sizeX) * (WIDTH // RECT_WIDTH), (playerY - camY + sizeY) * (HEIGHT // RECT_HEIGHT)))
    pygame.display.flip()
    clock.tick(FRAMERATE)