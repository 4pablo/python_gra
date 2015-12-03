#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, obiekt
from obiekt import *
from random import randint

pygame.init()
pygame.mixer.init()


class Gra:

    #obiekty
    mapa = obiekt("images/droga.jpg")
    paski = obiekt("images/paski.png")
    drzewo = obiekt("images/drzewa.png")
    glosnik = obiekt("grafika/audio.png", 735, 5)
    krzyzyk = obiekt("grafika/off.png", 735, 5)
    auto = obiekt("images/auto.png", 440, 460)
    paliwo = obiekt("grafika/gas.png")
    paliwo.przeksztalcObraz(64, 64)
    paliwo.ustawStatus()

    obiekty = [mapa, paski, drzewo, auto, glosnik]

    #utworzenie przeszkód
    samochody = []

    for i in range(2, 7):
        samochody.append(obiekt("grafika/auto" + str(i) + ".png"))

    #booleany
    wycisz = False
    oczekuj = False
    start = False
    koniec = False
    wyjdz = False
    showTime = False
    status = True

    #zmienne pomocnicze
    losujAuto = 0
    losujX = 0
    szybkosc = 20
    addTime = 0
    j=0
    i=0
    k=0
    l=0
    m=0
    autoSzybkosc=20
    predkoscPaliwa = 0
    time = 20 #czas gry (paliwo)

    #timer
    timer = USEREVENT + 1
    pygame.time.set_timer(timer, 1000)

    def graj(self):

        #muzyka
        self.ladujMuzyke('muzyka.mp3')

        #utowrzenie ekranu
        screen = self.utworzEkran(800,600, 'Samochody')

        #przygotowanie początkowego napisu
        self.ekranPoczatkowy(screen)

        #główna pętla
        while 1:
            #oczekiwanie na start
            while self.start == False:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key==pygame.K_SPACE:
                            self.start = True
                            pygame.mixer.music.play()

            #gra
            while self.koniec == False:

                #rysowanie podstawowych elementów (mapa, pas, drzewa, auto, glosnik)
                for obiekt in self.obiekty:
                    obiekt.rysuj(screen)

                # animacja pasow na drodze
                if self.i == self.szybkosc/3:
                    self.j += self.szybkosc/3
                    self.i = 0
                self.i += 1
                if self.j > self.szybkosc * 5:
                    self.j = 0

                self.paski.ustawPozycje(0, self.j - 100)

                #animacja drzew
                if self.l == self.szybkosc:
                    self.k += self.szybkosc
                    self.l = 0
                self.l += 1
                if self.k > self.szybkosc*90:
                    self.k=0

                self.drzewo.ustawPozycje(0, self.k-1100)

                #przeszkody
                for samochod in self.samochody:
                    if samochod.zwrocStatus == True:
                        self.status = False
                        break

                if self.status:
                    self.status = False
                    self.losujAuto = randint(0, 4)
                    self.losujX = randint(120,600)
                    self.samochody[self.losujAuto].ustawPozycje(self.losujX, -150)
                    self.samochody[self.losujAuto].ustawStatus(True)

                if self.samochody[self.losujAuto].zwrocY() > 600:
                    self.samochody[self.losujAuto].ustawStatus()
                    self.status = True

                if self.m<self.autoSzybkosc/2:
                    self.samochody[self.losujAuto].przesunY(self.autoSzybkosc/2)
                elif self.m>self.autoSzybkosc/2:
                    self.m=0
                self.m += 1
                self.samochody[self.losujAuto].rysuj(screen)

                #PALIWO
                losuj = randint(0,1000)
                if self.paliwo.zwrocStatus() == False and losuj < 5:
                    self.paliwo.ustawPozycje(randint(120,600), -64)
                    self.predkoscPaliwa = randint(20,50) / 10
                    self.paliwo.ustawStatus(True)

                if self.paliwo.zwrocY()>600:
                    self.paliwo.ustawStatus()

                if self.paliwo.zwrocStatus() == True:
                    self.paliwo.rysuj(screen)
                    self.paliwo.przesunY(self.predkoscPaliwa)

                #odejmij sekunde od czasu
                if pygame.event.get(self.timer):
                    if self.time > 1:
                        self.time -= 1
                    else:
                        self.koniec = True
                        self.time = 0
                    if self.showTime:
                        self.addTime += 1
                    if self.addTime == 2:
                        self.showTime = False
                        self.addTime = 0

                #odświeżanie czasu
                timeMessage = self.ustawCzcionke("ARCADECLASSIC.TTF", 30).render("paliwo ", 1, (255,255,255), (0, 0, 0))
                screen.blit(timeMessage, (0, 0))

                #dodaj 0 do czasu jeśli mniejsze od 10 (09 zamiast 9)
                if(self.time<10):
                    timeMessage = self.ustawCzcionke("ARCADECLASSIC.TTF", 30).render("0" + str(self.time), 1, (255,255,255), (0, 0, 0))

                else:
                    timeMessage = self.ustawCzcionke("ARCADECLASSIC.TTF", 30).render(str(self.time), 1, (255,255,255), (0, 0, 0))
                screen.blit(timeMessage, (35, 30))

                if self.showTime == True:
                    addTime = self.ustawCzcionke(None, 32).render("+3", 1, (255, 0, 255))
                    screen.blit(addTime, (self.auto.zwrocX()+70, self.auto.zwrocY()+20))


                #włączanie/wyłaczanie muzyki
                x, y = pygame.mouse.get_pos()

                if x > 743 and x < 760 and y > 9 and y < 35 and pygame.mouse.get_pressed()[0] and self.wycisz == False:
                    self.oczekuj = True

                elif x > 743 and x < 760 and y > 9 and y < 35 and pygame.mouse.get_pressed()[0] and self.wycisz == True :
                    self.oczekuj = False

                if self.oczekuj and pygame.mouse.get_pressed()[0] == 0:
                    self.wycisz = True
                if self.oczekuj == False and pygame.mouse.get_pressed()[0] == 0:
                    self.wycisz = False

                if self.wycisz:
                    self.krzyzyk.rysuj(screen)
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

            #kolizja
                #samochodu
                if self.auto.zwrocY() <= self.samochody[self.losujAuto].zwrocY()+137 and\
                        (self.auto.zwrocX()+50 >= self.losujX and self.auto.zwrocX() <= self.losujX+50) or time == 0:
                    self.koniec = True

                #paliwa
                if self.auto.zwrocY() <= self.paliwo.zwrocY()+64 and\
                        (self.auto.zwrocX()+50 >= self.paliwo.zwrocX() and self.auto.zwrocX() <= self.paliwo.zwrocX()+64):
                    self.paliwo.ustawStatus()
                    self.paliwo.ustawPozycje(0, 0)
                    self.time += 3
                    self.showTime = True

                #odświeżanie ekranu
                pygame.display.flip()

                #iwenty czyli sterowanie
                keys = pygame.key.get_pressed()
                if keys[K_LEFT]:
                    if self.auto.zwrocX()>120:
                        self.auto.ustawPozycje(self.auto.zwrocX()-5, 460)
                if keys[K_RIGHT]:
                    if self.auto.zwrocX()<620:
                        self.auto.ustawPozycje(self.auto.zwrocX()+5, 460)

                if keys[K_ESCAPE]:
                    pygame.quit()

                for event in pygame.event.get():
                    #wyłaczanie przez X
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        exit(0)


        #przegrana
            #napisy
            finishMessage = self.ustawCzcionke("ARCADECLASSIC.TTF", 64).render("GAME  OVER", 1, (255,255,255), (0,0,0))
            screen.blit(finishMessage, (260, 200))
            finishMessage = self.ustawCzcionke("ARCADECLASSIC.TTF", 32).render("SPACE  TO  NEW  GAME", 1, (255,255,255), (0,0,0))
            screen.blit(finishMessage, (270, 270))
            finishMessage = self.ustawCzcionke("ARCADECLASSIC.TTF", 32).render("ESC  TO  QUIT", 1, (255,255,255), (0,0,0))
            screen.blit(finishMessage, (320, 310))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #restart
                    if event.key==pygame.K_SPACE:
                        self.koniec = False
                        self.auto.ustawPozycje(440, 460)
                        self.samochody[self.losujAuto].ustawStatus()
                        self.status = True
                        self.statusPaliwa = 0
                        self.time = 20
                        self.paliwo.ustawStatus()
                        self.showTime = False

                    #wyjscie z gry
                    if event.key==pygame.K_ESCAPE:
                        pygame.quit()
                        exit(0)

    def ladujMuzyke(self, sciezka):
        pygame.mixer.music.load(sciezka)

    def utworzEkran(self, w, h, nazwa):
        screen=pygame.display.set_mode((w, h))
        pygame.display.set_caption(nazwa)
        return screen

    def ustawCzcionke(self, sciezka, rozmiar):
        return pygame.font.Font(sciezka, rozmiar)

    def ekranPoczatkowy(self, ekran):
        startMessage = self.ustawCzcionke("ARCADECLASSIC.TTF", 32).render("press  space  to  start", 1, (255,255,255))
        ekran.blit(startMessage, (250, 270))
        pygame.display.flip()