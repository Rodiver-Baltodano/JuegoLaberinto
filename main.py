import pygame
import sys
from pygame.locals import *
from random import randint

# Inicializar todos los módulos de Pygame (necesario antes de usar cualquier función)
pygame.init()

# Configurar la ventana
ancho = 1000  # Ancho de la ventana en píxeles
alto = 800  # Alto de la ventana en píxeles
ventana = pygame.display.set_mode((ancho, alto))  # Crea la ventana con las dimensiones especificadas
pygame.display.set_caption("Laberinto")  # Establece el título que aparece en la barra de la ventana

# Colores en formato RGB (Rojo, Verde, Azul) - cada valor va de 0 a 255
VERDE_OSCURO = (0, 128, 0)  # Verde oscuro para el fondo
GRIS = (40, 40, 40)  # Gris muy oscuro para las líneas del grid
colorJugador = (255,255,255)
colorMuro = (70,130,255)
colorLiana = (255, 255, 0)
colorTunel = (76,40,130)
colorMina = (255,0,0)

#Variables globales
velocidad = 1

#Mapa
world_data = []

#Listas de grupo
wall_group = pygame.sprite.Group()
liana_group = pygame.sprite.Group()
tunel_group = pygame.sprite.Group()
mina_group = pygame.sprite.Group()
spawn_position = ()

# Configuración del grid
tamano_celda = 40  # Cada celda medirá 40x40 píxeles
filas = alto // tamano_celda  # Calcula cuántas filas caben en la ventana (600 / 40 = 15 filas)
columnas = ancho // tamano_celda  # Calcula cuántas columnas caben en la ventana (800 / 40 = 20 columnas)

# Crear matriz del mapa: una lista de listas que representa el grid
# Cada posición [fila][columna] puede guardar un valor (0 = vacío por ahora)
mapa = [[0 for _ in range(columnas)] for _ in range(filas)]

# Reloj para controlar los FPS (frames por segundo)
reloj = pygame.time.Clock()

######################

#Clase de personajes
class personaje:
    def __init__(self, x, y, color, clase, cantidadMinas):
        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.Surface((tamano_celda, tamano_celda))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.clase = clase
        self.cantidadMinas = cantidadMinas

    #Actualiza el personaje dentro del grid    
    def update(self):
        self.image.fill(self.color)

        self.rect.x = self.x * tamano_celda
        self.rect.y = self.y * tamano_celda

        ventana.blit(self.image, self.rect)

    #Revisa si hay colisiones
    def colisionMuro(self):
        for muro in wall_group:
            if muro.x == self.x and muro.y == self.y:
                return True
        return False
    
    def colisionLiana(self):
        if self.clase == "cazador":
            return False
        else:
            for liana in liana_group:
                if liana.x == self.x and liana.y == self.y:
                    return True
            return False
        
    def colisionTunel(self):
        if self.clase == "presa":
            return False
        else:
            for tunel in tunel_group:
                if tunel.x == self.x and tunel.y == self.y:
                    return True
            return False
    
    def colocarMina(self):
        if self.cantidadMinas > 0:
            self.cantidadMinas -= 1
            Mina = mina(self.x, self.y, colorMina)
            mina_group.add(Mina)
        else:
            pass


#Clase de Muros
class muros(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()

        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.Surface((tamano_celda, tamano_celda))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x * tamano_celda
        self.rect.y = self.y * tamano_celda

class mina(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()

        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.Surface((tamano_celda, tamano_celda))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x * tamano_celda
        self.rect.y = self.y * tamano_celda



####################
#Lee el mapa del texto
with open('mapaPrueba.txt','r') as world:
    for line in world:
        world_data.append(line.strip())

#Lee que es un camino, que es el personaje, que es un muro, etc.
for row, tiles in enumerate(world_data):
    for col, tile in enumerate(tiles):
        if tile == '1':
            muro = muros(row, col, colorMuro)
            wall_group.add(muro)
        if tile == '2':
            liana = muros(row, col, colorLiana)
            liana_group.add(liana)
        if tile == '3':
            tunel = muros(row, col, colorTunel)
            tunel_group.add(tunel)
        if tile == 'P':
            spawn_position = (row, col)
        
#Define los personajes (Jugador, enemigos)
jugador = personaje(spawn_position[0], spawn_position[1], colorJugador, clase="cazador", cantidadMinas=3)

def dibujar_grid():
    """
    Dibuja las líneas de la cuadrícula sobre la ventana.
    Traza líneas verticales y horizontales para formar el grid.
    """
    # Dibujar líneas verticales
    for x in range(0, ancho, tamano_celda):  # Va desde 0 hasta ancho, saltando cada tamano_celda píxeles
        # pygame.draw.line(superficie, color, punto_inicio, punto_fin, grosor)
        pygame.draw.line(ventana, GRIS, (x, 0), (x, alto), 1)  # Línea de arriba a abajo
    
    # Dibujar líneas horizontales
    for y in range(0, alto, tamano_celda):  # Va desde 0 hasta alto, saltando cada tamano_celda píxeles
        pygame.draw.line(ventana, GRIS, (0, y), (ancho, y), 1)  # Línea de izquierda a derecha

#Define el movimiento del jugador
def movimiento():
    global velocidad
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] == True :
        jugador.x -= velocidad
        if jugador.colisionMuro() or jugador.colisionLiana() or jugador.colisionTunel(): #Devuelve al jugador si no puede pasar por un camino
            jugador.x += velocidad
        elif jugador.x < 0:
            jugador.x = 0
        
    elif key[pygame.K_RIGHT] == True :
        jugador.x += velocidad
        if jugador.x > (1000 - 40):
            jugador.x = (1000 - 40)
        elif jugador.colisionMuro() or jugador.colisionLiana() or jugador.colisionTunel():
            jugador.x -= velocidad

    elif key[pygame.K_UP]== True :
        jugador.y -= velocidad
        if jugador.y < 0:
            jugador.y = 0
        if jugador.colisionMuro() or jugador.colisionLiana() or jugador.colisionTunel():
            jugador.y += velocidad

    elif key[pygame.K_DOWN]== True :
        jugador.y += velocidad
        if jugador.y > (800 - 40):
                jugador.y = (800 - 40)
        if jugador.colisionMuro() or jugador.colisionLiana() or jugador.colisionTunel():
            jugador.y -= velocidad
    elif key[pygame.K_SPACE]== True:
        jugador.colocarMina()




<<<<<<< HEAD
    elif key[pygame.K_a] == True :
        jugador.x -= velocidad
        if jugador.colisionMuro() or jugador.colisionLiana() or jugador.colisionTunel(): 
            jugador.x += velocidad
        elif jugador.x < 0:
            jugador.x = 0
        
    elif key[pygame.K_d] == True :
        jugador.x += velocidad
        if jugador.x > (1000 - 40):
            jugador.x = (1000 - 40)
        elif jugador.colisionMuro() or jugador.colisionLiana() or jugador.colisionTunel():
            jugador.x -= velocidad

    elif key[pygame.K_w]== True :
        jugador.y -= velocidad
        if jugador.y < 0:
            jugador.y = 0
        if jugador.colisionMuro() or jugador.colisionLiana() or jugador.colisionTunel():
            jugador.y += velocidad

    elif key[pygame.K_s]== True :
        jugador.y += velocidad
        if jugador.y > (800 - 40):
                jugador.y = (800 - 40)
        if jugador.colisionMuro() or jugador.colisionLiana() or jugador.colisionTunel():
            jugador.y -= velocidad

    elif key[pygame.K_SPACE]== True:
        jugador.colocarMina()




=======
>>>>>>> 8c37bfe3ae958ec490b6b6e84f3287ea3c1ed009

##################################
# Bucle principal del juego - se ejecuta continuamente hasta que se cierra la ventana
ejecutando = True
while ejecutando:
    ventana.fill(VERDE_OSCURO)
    wall_group.draw(ventana)
    liana_group.draw(ventana)
    tunel_group.draw(ventana)
    mina_group.draw(ventana)
    movimiento() #Revisa por movimiento
    # Procesar todos los eventos que ocurren (clicks, teclas, cierre de ventana, etc.)
    for evento in pygame.event.get():  # Obtiene lista de todos los eventos ocurridos desde el último frame
        if evento.type == pygame.QUIT:  # Si el usuario cierra la ventana (click en X)
            ejecutando = False  # Cambia la bandera para salir del bucle
    # Dibujar todo en la ventana
    
    
    dibujar_grid()  # Llama a la función que dibuja las líneas del grid

    
    jugador.update() #Actualiza el jugador
    

    # Actualizar la pantalla para mostrar los cambios
    pygame.display.flip()  # Actualiza toda la pantalla con lo que se dibujó
    
    # Controlar la velocidad del juego
    reloj.tick(10)  # Limita el bucle a 60 iteraciones por segundo (60 FPS)

# Cerrar Pygame correctamente
pygame.quit()  # Cierra todos los módulos de Pygame
sys.exit()  # Termina el programa completamente