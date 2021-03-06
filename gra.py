#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, obiekt, bitmapa, prostokat, os.path
from obiekt import *
from bitmapa import *
from prostokat import *
from random import randint

pygame.init()
pygame.mixer.init()


class Gra:

    #obiekty
    mapa = Bitmapa("images/droga.jpg")
    paski = Bitmapa("images/paski.png")
    drzewo = Bitmapa("images/drzewa.png")
    glosnik = Bitmapa("grafika/audio.png", 735, 5)
    krzyzyk = Bitmapa("grafika/off.png", 735, 5)
    auto = Bitmapa("images/auto.png", 440, 460)
    paliwo = Bitmapa("grafika/gas.png")
    paliwo.przeksztalcObraz(64, 64)
    paliwo.ustawStatus()
    prostokat = Prostokat((0, 0, 0), 36, 36, 733, 3)

    obiekty = [mapa, paski, drzewo, auto, prostokat, glosnik]

    #utworzenie przeszkód
    samochody = []

    for i in range(2, 7):
        samochody.append(Bitmapa("grafika/auto" + str(i) + ".png"))

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
    wynik = 0
    sekunda = 0

    #timer
    timer = USEREVENT + 1
    pygame.time.set_timer(timer, 100)

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
                            pygame.mixer.music.play(-1)

            #gra
            while self.koniec == False:

                #rysowanie podstawowych elementów (mapa, pas, drzewa, auto, glosnik)
                for obiekt in self.obiekty:
                    obiekt.rysuj(screen)

                #prostokąty
                #pygame.draw.rect(screen, (0, 0, 0), (0, 0, 105, 60))
                #pygame.draw.rect(screen, (0, 0, 0), (0, 540, 105, 60))

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
                if self.paliwo.zwrocStatus() == False and losuj < 7:
                    self.paliwo.ustawPozycje(randint(120,600), -64)
                    self.predkoscPaliwa = randint(20,50) / 10
                    self.paliwo.ustawStatus(True)

                if self.paliwo.zwrocY()>600:
                    self.paliwo.ustawStatus()
                    self.paliwo.ustawPozycje(0,0)

                if self.paliwo.zwrocStatus() == True:
                    self.paliwo.rysuj(screen)
                    self.paliwo.przesunY(self.predkoscPaliwa)

                #odejmij sekunde od czasu
                if pygame.event.get(self.timer):
                    self.wynik += 1
                    if self.sekunda < 10:
                        self.sekunda += 1
                    else:
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
                        self.sekunda = 0

                #odświeżanie czasu
                timeMessage = self.ustawCzcionke("ARCADECLASSIC.TTF", 30).render("paliwo ", 1, (255,255,255))
                screen.blit(timeMessage, (0, 0))

                #dodaj 0 do czasu jeśli mniejsze od 10 (09 zamiast 9)
                if(self.time<10):
                    timeMessage = self.ustawCzcionke("ARCADECLASSIC.TTF", 30).render("0" + str(self.time), 1, (255,255,255))

                else:
                    timeMessage = self.ustawCzcionke("ARCADECLASSIC.TTF", 30).render(str(self.time), 1, (255,255,255))
                screen.blit(timeMessage, (35, 30))

                if self.showTime == True:
                    addTime = self.ustawCzcionke(None, 32).render("+5", 1, (255, 0, 255))
                    screen.blit(addTime, (self.auto.zwrocX()+70, self.auto.zwrocY()+20))

                #punkty
                napis = self.ustawCzcionke("ARCADECLASSIC.TTF", 30).render("wynik", 1, (255, 255, 255))
                screen.blit(napis, (0, 540))

                pkt =  self.ustawCzcionke("ARCADECLASSIC.TTF", 30).render(str(self.wynik), 1, (255, 255, 255))
                screen.blit(pkt, (0, 570))

                #najlepszy wynik
                if(os.path.exists("wyniki.bin")):
                        with open("wyniki.bin", "r") as f:
                            best = f.read()
                else:
                    best = 0

                napis = self.ustawCzcionke("ARCADECLASSIC.TTF", 30).render("best", 1, (255, 255, 255))
                screen.blit(napis, (700, 540))

                pkt =  self.ustawCzcionke("ARCADECLASSIC.TTF", 30).render(str(best), 1, (255, 255, 255))
                screen.blit(pkt, (700, 570))

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
                    self.time += 5
                    self.showTime = True

                #iwenty czyli sterowanie
                keys = pygame.key.get_pressed()
                if keys[K_LEFT]:
                    if self.auto.zwrocX()>120:
                        self.auto.ustawPozycje(self.auto.zwrocX()-5, 460)
                if keys[K_RIGHT]:
                    if self.auto.zwrocX()<620:
                        self.auto.ustawPozycje(self.auto.zwrocX()+5, 460)

                if keys[K_ESCAPE]:
                    return

                for event in pygame.event.get():
                    #wyłaczanie przez X
                    if event.type==pygame.QUIT:
                        return

                #zapisanie wyniku
                if(self.koniec):
                    if(os.path.exists("wyniki.bin")):
                        with open("wyniki.bin", "r") as f:
                            high = f.read()

                    else:
                        high = 0

                    if self.wynik > int(high):
                        with open('wyniki.bin', 'w') as f:
                            f.write(str(self.wynik))


                #odświeżanie ekranu
                pygame.display.update()



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
                        self.paliwo.ustawPozycje(0, 0)
                        self.showTime = False
                        self.wynik = 0

                    #wyjscie z gry
                    if event.key==pygame.K_ESCAPE:
                        return

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