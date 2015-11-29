# -*- coding: utf-8 -*-


# 1 - Import library
import pygame
import random
from pygame.locals import *
from random import randint
#jakies gowno do mesedzboksow
import ctypes  # An included library with Python install.


# 2 - Initialize the game
pygame.init()
width, height = 800, 600
screen=pygame.display.set_mode((width, height))
pygame.display.set_caption('Samochody')
clock = pygame.time.Clock()


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
k=0
l=0
iloscDrzew=0
czas = 0.0

paliwo = 10 #czas w sekundach
pygame.time.set_timer(USEREVENT+1, 1000)#1 sekunda=1000milisekund

# 4 - keep looping through
while 1:
    # 5 - clear the screen before drawing it again
    screen.fill(0)
    # 6 - draw the screen elements
    screen.blit(mapa, (0,0))
    #paliwo

    for event in pygame.event.get():
        if event.type == USEREVENT+1:
            paliwo -= 1
       # elif paliwo == 0:
            #ctypes.windll.user32.MessageBoxA(0, "Skonczylo sie paliwo".format(czas), "Wynik", 0)
            #pygame.quit()
    # animacja pasow na drodze
    if i==szybkosc/3:
        j=j+szybkosc/3
        i=0
    screen.blit(paski, (0,j-100))
    i=i+1
    if j>szybkosc*5:
        j=0
    #animacja drzew
    if l==szybkosc:
        k=k+szybkosc
        l=0
    l=l+1
    if k>szybkosc*85:
        k=0
    screen.blit(drzewo, (0,k-1100))

    screen.blit(auto, (pozycjaX,pozycjaY))
    clock.tick(60)




    # 7 - update the screen
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
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()


        # check if the event is the X button

        if event.type==pygame.QUIT:
            # Czas i punkty.
            ctypes.windll.user32.MessageBoxA(0, "Twoj wynik to: {0:.2f} sekundy".format(czas), "Wynik", 0)
            # if it is quit the game
            pygame.quit()
            exit(0)
