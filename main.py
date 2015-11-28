# 1 - Import library
import pygame
import random
from pygame.locals import *
from random import randint


# 2 - Initialize the game
pygame.init()
width, height = 800, 600
screen=pygame.display.set_mode((width, height))
 
# 3 - Load images
mapa = pygame.image.load("images/droga.jpg")
auto = pygame.image.load("images/auto.png")
paski = pygame.image.load("images/paski.png")
drzewo = pygame.image.load("images/drzewa.png")
pozycjaX = 440
pozycjaY = 460
szybkosc = 20
j=0
i=0
p=-600
iloscDrzew=0

#sadasdasdasd

#clock=pygame.time.Clock()
# 4 - keep looping through
while 1:
    # 5 - clear the screen before drawing it again
    screen.fill(0)
    # 6 - draw the screen elements
    screen.blit(mapa, (0,0))
    # animacja pasow na drodze
    if i==szybkosc/3:
        j=j+szybkosc/3
        i=0
    screen.blit(paski, (0,j-100))
    i=i+1
    if j>szybkosc*5:
        j=0

    screen.blit(auto, (pozycjaX,pozycjaY))

    screen.blit(drzewo, (0,-500))


    # 7 - update the screen
    #clock.tick(60)
    pygame.display.flip()
    # 8 - loop through the events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key==K_LEFT:
                if pozycjaX>120:
                    pozycjaX=pozycjaX-20
            elif event.key==K_RIGHT:
                if pozycjaX<620:
                    pozycjaX=pozycjaX+20
        # check if the event is the X button 
        if event.type==pygame.QUIT:
            # if it is quit the game
            pygame.quit() 
            exit(0)
