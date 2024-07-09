#! python 3
# Sprite Implementation for the AI Dungeon Crawler, Currently Non-functional
import pygame, sys

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