import pygame_light2d as pl2d, pygame
from pygame_light2d import LightingEngine, PointLight, Hull

pygame.init()
screen_res = (1280, 720)
lights_engine = LightingEngine(
    screen_res=screen_res, native_res=screen_res, lightmap_res=(int(screen_res[0]/2.5), int(screen_res[1]/2.5)))