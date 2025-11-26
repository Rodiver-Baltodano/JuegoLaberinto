import pygame
import sys
from pygame.locals import *
from random import randint
import random


# Inicializar todos los módulos de Pygame (necesario antes de usar cualquier función)
pygame.init()

# Configurar la ventana
ancho = 1000  # Ancho de la ventana en píxeles
alto = 800  # Alto de la ventana en píxeles
ventana = pygame.display.set_mode((ancho, alto))  # Crea la ventana con las dimensiones especificadas
pygame.display.set_caption("Laberinto")  # Establece el título que aparece en la barra de la ventana

# Configuración del grid
tamano_celda = 40  # Cada celda medirá 40x40 píxeles
filas = alto // tamano_celda  # Calcula cuántas filas caben en la ventana (600 / 40 = 15 filas)
columnas = ancho // tamano_celda  # Calcula cuántas columnas caben en la ventana (800 / 40 = 20 columnas)

VERDE_OSCURO = (0, 128, 0)  
GRIS = (40, 40, 40)  
colorJugador = (255,255,255)
colorEnemigo = (255, 0, 0)
colorMina = (255,165,0)

liana_image = pygame.image.load('imagenes/liana.png')
liana_image = pygame.transform.scale(liana_image, (tamano_celda, tamano_celda))

muro_image = pygame.image.load('imagenes/muro.png')
muro_image = pygame.transform.scale(muro_image, (tamano_celda, tamano_celda))

tunel_image = pygame.image.load('imagenes/tunel.png')
tunel_image = pygame.transform.scale(tunel_image, (tamano_celda, tamano_celda))

Fondo = pygame.image.load('imagenes/Fondo.png')
Fondo = pygame.transform.scale(Fondo, (ancho, alto))

fuente_grande = pygame.font.Font(None, 74)
fuente_mediana = pygame.font.Font(None, 36)


#Variables globales
velocidad = 1
GRID_COLS = 25
GRID_ROWS = 20
    
MAX_TUNELES = 5
MAX_LIANAS = 5
MAX_MUROS = 10


#Mapa
world_data = []

#Listas de grupo
wall_group = pygame.sprite.Group()
liana_group = pygame.sprite.Group()
tunel_group = pygame.sprite.Group()
mina_group = pygame.sprite.Group()
spawn_position = []  
En1Spawn_Position = []


# Crear matriz del mapa: una lista de listas que representa el grid
# Cada posición [fila][columna] puede guardar un valor (0 = vacío por ahora)
mapa = [[0 for _ in range(columnas)] for _ in range(filas)]

# Reloj para controlar los FPS (frames por segundo)
reloj = pygame.time.Clock()

######################


#####################
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
    
    #Coloca minas
    def colocarMina(self):
        if self.cantidadMinas > 0:
            self.cantidadMinas -= 1
            Mina = mina(self.x, self.y, colorMina)
            mina_group.add(Mina)
        else:
            pass

    def colisionMina(self):
        if self.clase == "presa":
            return False
        else:
            for Mina in mina_group:
                if Mina.x == self.x and Mina.y == self.y:
                    return True
            return False

    

#Clase de Muros
class muros(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.x = x
        self.y = y
        self.image = image.copy()
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
class Mapa:
    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.map_data: list[list[str]]

        
    def generate_map(self):
        self.map_data = [[0 for _ in range(self.width)] for _ in range(self.height)]

        map_data = []
        for row in range(self.height):
            row_data = []
            for col in range(self.width):
                row_data.append(0)
            map_data.append(row_data)

    def generate_patch(self, tile, num_patches, min, max, irregular):
        for _ in range(num_patches):
            width = randint(min, max)
            height = randint(min, max)
            start_x = randint(1, self.width - width - 1)
            start_y = randint(1, self.height - height - 1)

            if irregular == True:
                init_start_x = randint(3, self.width - max)

            for i in range(height):
                if min != max:  
                    width = randint(int(0.7* max), max)
                if irregular == True:
                    start_x = init_start_x - randint(1,2)
                for j in range(width):
                    self.map_data[start_y + i][start_x + j] = tile



####################
def generar_mapa():
    global mapaRandom
    global wall_group, liana_group, tunel_group, spawn_position, En1Spawn_Position
    mapaRandom = Mapa(GRID_ROWS, GRID_COLS)

    mapaRandom.generate_map()
    mapaRandom.generate_patch(1, MAX_MUROS, 2, 3, False)
    mapaRandom.generate_patch(2, MAX_LIANAS, 2, 3, True)
    mapaRandom.generate_patch(3, MAX_TUNELES, 2, 3, True)
    mapaRandom.generate_patch(4, 1, 1, 1, False)
    mapaRandom.generate_patch(5, 1, 1, 1, False)

    print(mapaRandom)
    #Lee que es un camino, que es el personaje, que es un muro, etc.
    for row, tiles in enumerate(mapaRandom.map_data):
        for col, tile in enumerate(tiles):  
            if tile == 1:  
                muro = muros(row, col, muro_image)
                wall_group.add(muro)
            if tile == 2:
                liana = muros(row, col, liana_image)
                liana_group.add(liana)
            if tile == 3:
                tunel = muros(row, col, tunel_image)
                tunel_group.add(tunel)
            if tile == 4:  
                spawn_position = [row, col]
            if tile == 5:
                En1Spawn_Position = [row, col]

    if not spawn_position:
        spawn_position = [0, 0]

generar_mapa()
#Define los personajes (Jugador, enemigos)
jugador = personaje(spawn_position[0], spawn_position[1], colorJugador, clase="presa", cantidadMinas=3)
enemigo1 = personaje(En1Spawn_Position[0], En1Spawn_Position[1], colorEnemigo, clase="cazador", cantidadMinas=0)

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
        if jugador.x > 24:
            jugador.x = 24
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
        if jugador.y > 19:
                jugador.y = 19
        if jugador.colisionMuro() or jugador.colisionLiana() or jugador.colisionTunel():
            jugador.y -= velocidad
    

    elif key[pygame.K_a] == True :
        jugador.x -= velocidad
        if jugador.colisionMuro() or jugador.colisionLiana() or jugador.colisionTunel(): 
            jugador.x += velocidad
        elif jugador.x < 0:
            jugador.x = 0
        
    elif key[pygame.K_d] == True :
        jugador.x += velocidad
        if jugador.x > 24:
            jugador.x = 24
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
        if jugador.y > 19:
                jugador.y = 19
        if jugador.colisionMuro() or jugador.colisionLiana() or jugador.colisionTunel():
            jugador.y -= velocidad

    elif key[pygame.K_SPACE]== True:
        jugador.colocarMina()

def movimientoEnemigo(self, objetivo):
    global velocidad
    direccion = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
    tiempo_cambio_direccion = pygame.time.get_ticks()
    intervalo_cambio = random.randint(1000, 3000)
    modo_persecucion = False
    tiempo_ultima_persecucion = pygame.time.get_ticks()
    tiempo_inicio_persecucion = 0

    tiempo_actual = pygame.time.get_ticks()
        
    # Activar persecución cada 10 segundos por 3 segundos
    if tiempo_actual - tiempo_ultima_persecucion >= 10000:
        modo_persecucion = True
        tiempo_inicio_persecucion = tiempo_actual
        tiempo_ultima_persecucion = tiempo_actual
        
    if modo_persecucion and tiempo_actual - tiempo_inicio_persecucion >= 3000:
        modo_persecucion = False
        
    # Posición anterior para revertir en caso de colisión
    pos_anterior = (self.x, self.y)
        
    if modo_persecucion:
        # Mover hacia el objetivo
        dx, dy = objetivo.x - self.x, objetivo.y - self.y
        if abs(dx) > abs(dy):
            self.x += velocidad if dx > 0 else -velocidad
        else:
            self.y += velocidad if dy > 0 else -velocidad
    else:
        # Movimiento aleatorio
        if tiempo_actual - tiempo_cambio_direccion >= intervalo_cambio:
            direccion = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
            tiempo_cambio_direccion = tiempo_actual
            intervalo_cambio = random.randint(1000, 3000)
            
        # Aplicar movimiento
        if direccion == 'LEFT':
            self.x -= velocidad
        elif direccion == 'RIGHT':
            self.x += velocidad
        elif direccion == 'UP':
            self.y -= velocidad
        elif direccion == 'DOWN':
            self.y += velocidad
        
    # Revertir si hay colisión
    if self.colisionMuro() or self.colisionLiana() or self.colisionTunel() or self.x < 0 or self.x > 24 or self.y < 0 or self.y > 19:    
        self.x, self.y = pos_anterior
    if not modo_persecucion:
        direccion = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])

        
    # Ajustar dirección si se alcanza un borde
    if self.x == 0:
        direccion = 'RIGHT'
    elif self.x == 24:
        direccion = 'LEFT'
    if self.y == 0:
        direccion = 'DOWN'
    elif self.y == 19:
        direccion = 'UP'

##################################
# Bucle principal del juego - se ejecuta continuamente hasta que se cierra la ventana
ejecutando = True
juego_terminado = False

while ejecutando:
    ventana.blit(Fondo, (0,0))
    wall_group.draw(ventana)
    liana_group.draw(ventana)
    tunel_group.draw(ventana)
    mina_group.draw(ventana)
    

    # Procesar todos los eventos que ocurren (clicks, teclas, cierre de ventana, etc.)
    for evento in pygame.event.get():  # Obtiene lista de todos los eventos ocurridos desde el último frame
        if evento.type == pygame.QUIT:  # Si el usuario cierra la ventana (click en X)
            ejecutando = False  # Cambia la bandera para salir del bucle
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r and juego_terminado:
                # Reiniciar juego
                juego_terminado = False
                
                jugador.x, jugador.y = spawn_position[0], spawn_position[1]
                enemigo1.x, enemigo1.y = En1Spawn_Position[0], En1Spawn_Position[1]
                wall_group = pygame.sprite.Group()
                liana_group = pygame.sprite.Group()
                tunel_group = pygame.sprite.Group()
                mina_group = pygame.sprite.Group()
                spawn_position = []  
                En1Spawn_Position = []
                generar_mapa()
    
    
    dibujar_grid()  # Llama a la función que dibuja las líneas del grid
    if not juego_terminado:
        movimiento() #Revisa por movimiento
        movimientoEnemigo(enemigo1, jugador)
        if enemigo1.colisionMina() == True:
            enemigo1.kill()
        if jugador.x == enemigo1.x and jugador.y == enemigo1.y:
            juego_terminado = True
        jugador.update() #Actualiza el jugador
        enemigo1.update()

    if juego_terminado:
        # Fondo semi-transparente
        overlay = pygame.Surface((1000, 800))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        ventana.blit(overlay, (0, 0))
        
        # Texto Game Over
        texto_game_over = fuente_grande.render("GAME OVER", True, (255, 0, 0))
        texto_reiniciar = fuente_mediana.render("Presiona R para reiniciar", True, (255, 255, 255))
        
        rect_game_over = texto_game_over.get_rect(center=(1000 // 2, 800 // 2 - 50))
        rect_reiniciar = texto_reiniciar.get_rect(center=(1000 // 2, 800 // 2 + 50))
        
        ventana.blit(texto_game_over, rect_game_over)
        ventana.blit(texto_reiniciar, rect_reiniciar)
     
    
  
    # Actualizar la pantalla para mostrar los cambios
    pygame.display.flip()  # Actualiza toda la pantalla con lo que se dibujó
    
    # Controlar la velocidad del juego
    reloj.tick(10)  # Limita el bucle a 60 iteraciones por segundo (60 FPS)

# Cerrar Pygame correctamente
pygame.quit()  # Cierra todos los módulos de Pygame
sys.exit()  # Termina el programa completamente