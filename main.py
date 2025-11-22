import pygame  # Biblioteca para crear juegos y gráficos
import sys  # Biblioteca para interactuar con el sistema operativo

# Inicializar todos los módulos de Pygame (necesario antes de usar cualquier función)
pygame.init()

# Configurar la ventana
ancho = 800  # Ancho de la ventana en píxeles
alto = 600  # Alto de la ventana en píxeles
ventana = pygame.display.set_mode((ancho, alto))  # Crea la ventana con las dimensiones especificadas
pygame.display.set_caption("Grid Base")  # Establece el título que aparece en la barra de la ventana

# Colores en formato RGB (Rojo, Verde, Azul) - cada valor va de 0 a 255
VERDE_OSCURO = (0, 128, 0)  # Verde oscuro para el fondo
GRIS = (40, 40, 40)  # Gris muy oscuro para las líneas del grid

# Configuración del grid
tamano_celda = 40  # Cada celda medirá 40x40 píxeles
filas = alto // tamano_celda  # Calcula cuántas filas caben en la ventana (600 / 40 = 15 filas)
columnas = ancho // tamano_celda  # Calcula cuántas columnas caben en la ventana (800 / 40 = 20 columnas)

# Crear matriz del mapa: una lista de listas que representa el grid
# Cada posición [fila][columna] puede guardar un valor (0 = vacío por ahora)
mapa = [[0 for _ in range(columnas)] for _ in range(filas)]

# Reloj para controlar los FPS (frames por segundo)
reloj = pygame.time.Clock()

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

# Bucle principal del juego - se ejecuta continuamente hasta que se cierra la ventana
ejecutando = True
while ejecutando:
    # Procesar todos los eventos que ocurren (clicks, teclas, cierre de ventana, etc.)
    for evento in pygame.event.get():  # Obtiene lista de todos los eventos ocurridos desde el último frame
        if evento.type == pygame.QUIT:  # Si el usuario cierra la ventana (click en X)
            ejecutando = False  # Cambia la bandera para salir del bucle
    
    # Dibujar todo en la ventana
    ventana.fill(VERDE_OSCURO)  # Llena toda la ventana con el color verde oscuro (borra lo anterior)
    dibujar_grid()  # Llama a la función que dibuja las líneas del grid
    
    # Actualizar la pantalla para mostrar los cambios
    pygame.display.flip()  # Actualiza toda la pantalla con lo que se dibujó
    
    # Controlar la velocidad del juego
    reloj.tick(60)  # Limita el bucle a 60 iteraciones por segundo (60 FPS)

# Cerrar Pygame correctamente
pygame.quit()  # Cierra todos los módulos de Pygame
sys.exit()  # Termina el programa completamente