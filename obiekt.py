#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame import *

class obiekt:
    def __init__(self, obraz, x = 0, y = 0, status = False):
        self.obraz = pygame.image.load(obraz)
        self.x = x
        self.y = y
        self.status = status

    def rysuj(self, ekran):
        ekran.blit(self.obraz, (self.x, self.y))

    def ustawPozycje(self, x, y):
        self.x = x
        self.y = y

    def przesunY(self, przesuniecie):
        self.y += przesuniecie

    def zwrocX(self):
        return self.x

    def zwrocY(self):
        return self.y

    def ustawStatus(self, status = False):
        self.status = status

    def zwrocStatus(self):
        return self.status

    def przeksztalcObraz(self, w, h):
        self.obraz = pygame.transform.scale(self.obraz, (64, 64))