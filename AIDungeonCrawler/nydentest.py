import pygame

map = [['#','#','#','#','#'],
        ['#','#','#','#','#'],
        ['#','#','#','#','E'],
        ['#','#','#','#','#'],
        ['#','#','#','#','#']
       ]

FRAMERATE = 120
RECT_WIDTH = 5
RECT_HEIGHT = 5
WIDTH = 720
HEIGHT = 720


pygame.init()
screen = pygame.display.set_mode((WIDTH - 1, HEIGHT - 1))
pygame.display.set_caption('AI Dungeon Crawler')
clock = pygame.time.Clock()
running = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BLUE = (0, 0, 200)


playerX = 0
playerY = 0
def draw_pixels(arr):
    width_ratio = (WIDTH // RECT_WIDTH)
    height_ratio = (HEIGHT // RECT_HEIGHT)
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            if (y == playerX) and (x == playerY):
                pygame.draw.rect(screen, BLUE, pygame.Rect(y * width_ratio, x * height_ratio,
                                                            width_ratio - 1, height_ratio - 1))
            elif arr[x][y] == '#':
                pygame.draw.rect(screen, BLACK, pygame.Rect(y * width_ratio, x * height_ratio,
                                                            width_ratio - 1, height_ratio - 1))
            else:
                pygame.draw.rect(screen, WHITE, pygame.Rect(y * width_ratio, x * height_ratio,
                                                            width_ratio - 1, height_ratio - 1))


while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                playerX += 1
            if event.key == pygame.K_a:
                playerX -= 1
            if event.key == pygame.K_w:
                playerY -= 1
            if event.key == pygame.K_s:
                playerY += 1
    draw_pixels(map)
    pygame.display.flip()
    clock.tick(FRAMERATE)
