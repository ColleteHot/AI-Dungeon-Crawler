import pygame
# TODO When time allows, figure out reserved channels to hold one for backround music, in case of many sounds at once
# WARNING! THESE FUNCTIONS WILL SPAWN AN ERROR IF THE VARIABLES USED TO HOLD SOUND LOCATIONS CONTAIN NUMBERS
# TODO Try to complete impsoundF
# Pycharm Docs suck booty


# Sets the backround Music (Functional)
def musicPlay(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play(loops=True, start=0.0, fade_ms=10)

# Plays any type of sound/sfx (Functional)
def soundPlay(sound):
    sound = pygame.mixer.Sound(sound)
    pygame.mixer.Sound.play(sound, loops=False, fade_ms=10)

# Given a filepath, and a name, it will import the soundfile and give it a name (Non-Functional)
# def impsoundF(fname, name):
    #if name != '':
        #name = fname
        #soundList.append(name)
    #else:
        #name = fname
        #soundList.append(name)


pygame.mixer.init(frequency=44100, size=-16, channels=4, buffer=512, devicename=None)
pygame.mixer.set_reserved(0)
# soundList = []
# pygame.mixer.init()
# pygame.mixer.set_reserved(0)
# gameLoop = pygame.mixer.music.load('C:\\Users\\Student\\Desktop\\Github Repositories\\AI-Dungeon-Crawler\\AIDungeonCrawler\\Sound Files\\gameLoop.wav')
# pygame.mixer.music.play(loops=True, start=0.0, fade_ms=10)
# time.sleep(4)