#!/usr/bin/env python
# -*- coding: utf-8 -*-

import obiekt
from obiekt import *

class Prostokat(obiekt):

    def __init__(self, kolor, w, h, x = 0, y = 0):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.kolor = kolor

    def rysuj(self, ekran):
        pygame.draw.rect(ekran, self.kolor, (self.x, self.y, self.w, self.h))


#