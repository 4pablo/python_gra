import pygame

pygame.init()


display_width = 850
display_height = 650

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Samochody')

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed = False


autoImg = pygame.image.load('auto.png')
drogaImg = pygame.image.load('droga.jpg')

gameDisplay.blit(drogaImg, (0,0))

def car(x,y):
    gameDisplay.blit(autoImg, (x,y))

x =  (display_width * 0.45)
y = (display_height * 0.75)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill(white)
    car(x,y)

        
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
