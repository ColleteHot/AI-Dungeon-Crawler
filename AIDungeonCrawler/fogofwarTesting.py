import pygame, nydenstuff, time
pygame.init()

display = (1280,720)
screen = pygame.display.set_mode(display, 0, 32)
screen.fill((255,255,255)) # Fill the screen white so you can see when fog of war is lifted
fog_of_war = pygame.Surface(display)
fog_of_war.fill((0,0,0)) # creates surface size of the display and fills it black, nothing can be seen.
pygame.draw.circle(fog_of_war,(60,60,60),(200,200),100,0)
fog_of_war.set_colorkey((60,60,60)) #This is the important part, first we drew a circle on the fog of war with a certain color which we now set to transparent.
screen.blit(fog_of_war,(0,0))
pygame.display.update()
time.sleep(4)