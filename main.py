#
# Personaje
#

import pygame
import sys
from pygame.locals import *
from random import randint

pygame.init()
ventana = pygame.display.set_mode((1000,800))
pygame.display.set_caption("Laberinto")
colorFondo = (0, 0, 0)
colorFigura = (255,255,255)

posX, posY = randint(1,900), randint(1,700)
velocidad = 15

def movimiento():
    global posX, posY
    global velocidad
    key = pygame.key.get_pressed()
    if key[pygame.K_a] or key[pygame.K_LEFT] == True:
        posX -= velocidad
        if posX < 0:
            posX = 0
    elif key[pygame.K_d] or key[pygame.K_RIGHT] == True:
        posX += velocidad
        if posX > (1000 - 40):
            posX = (1000 - 40)
    elif key[pygame.K_w] or key[pygame.K_UP]== True:
        posY -= velocidad
        if posY < 0:
            posY = 0
    elif key[pygame.K_s] or key[pygame.K_DOWN]== True:
        posY += velocidad
        if posY > (800 - 40):
            posY = (800 - 40)


run = True
while run:
    ventana.fill(colorFondo)
    pygame.draw.rect(ventana, colorFigura, (posX, posY, 40, 40))
    #movimiento
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()
        movimiento()
    pygame.display.update()


