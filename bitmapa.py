#!/usr/bin/env python
# -*- coding: utf-8 -*-

import obiekt
from obiekt import *

class Bitmapa(obiekt):

    def __init__(self, obraz, x = 0, y = 0, status = False):
        self.obraz = pygame.image.load(obraz)
        self.x = x
        self.y = y
        self.status = status

    def rysuj(self, ekran):
        ekran.blit(self.obraz, (self.x, self.y))

    def przeksztalcObraz(self, w, h):
        self.obraz = pygame.transform.scale(self.obraz, (64, 64))