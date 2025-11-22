import pygame  # Biblioteca para crear juegos y gráficos
import sys  # Biblioteca para interactuar con el sistema operativo
import random  # Biblioteca para generar números aleatorios
import time  # Biblioteca para manejar tiempos

# Inicializar todos los módulos de Pygame (necesario antes de usar cualquier función)
pygame.init()

# Configurar la ventana
ancho = 800  # Ancho de la ventana en píxeles
alto = 600  # Alto de la ventana en píxeles
ventana = pygame.display.set_mode((ancho, alto))  # Crea la ventana con las dimensiones especificadas
pygame.display.set_caption("Juego con Enemigo IA")  # Establece el título que aparece en la barra de la ventana

# Colores en formato RGB (Rojo, Verde, Azul) - cada valor va de 0 a 255
VERDE_OSCURO = (0, 128, 0)  # Verde oscuro para el fondo
GRIS = (40, 40, 40)  # Gris muy oscuro para las líneas del grid
AZUL = (0, 100, 255)  # Color azul para el jugador
ROJO = (255, 50, 50)  # Color rojo para los enemigos
BLANCO = (255, 255, 255)  # Color blanco para texto

# Configuración del grid
tamano_celda = 40  # Cada celda medirá 40x40 píxeles
filas = alto // tamano_celda  # Calcula cuántas filas caben en la ventana (600 / 40 = 15 filas)
columnas = ancho // tamano_celda  # Calcula cuántas columnas caben en la ventana (800 / 40 = 20 columnas)

# Crear matriz del mapa: una lista de listas que representa el grid
# Cada posición [fila][columna] puede guardar un valor (0 = vacío por ahora)
mapa = [[0 for _ in range(columnas)] for _ in range(filas)]

# Reloj para controlar los FPS (frames por segundo)
reloj = pygame.time.Clock()

# Fuente para mostrar texto
fuente = pygame.font.Font(None, 48)  # Crea fuente de tamaño 48

# Clase para representar enemigos en el juego
class Enemigo:
    """
    Clase que representa un enemigo en el grid.
    Cada enemigo tiene una posición (fila, columna) y puede moverse de forma aleatoria
    o perseguir al jugador cada 8 segundos.
    """
    def __init__(self, fila, columna):
        """
        Constructor de la clase Enemigo.
        fila: posición vertical del enemigo en el grid
        columna: posición horizontal del enemigo en el grid
        """
        self.fila = fila  # Guarda la fila donde está el enemigo
        self.columna = columna  # Guarda la columna donde está el enemigo
        self.direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])  # Dirección inicial aleatoria
        self.tiempo_ultimo_cambio = time.time()  # Marca de tiempo del último cambio de dirección
        self.tiempo_ultima_busqueda = time.time()  # Marca de tiempo de la última vez que buscó al jugador
        self.velocidad_cambio = random.uniform(1.5, 3.0)  # Cada cuántos segundos cambia de dirección aleatoriamente
        self.buscando_jugador = False  # Indica si está persiguiendo al jugador
    
    def cambiar_direccion_aleatoria(self):
        """
        Cambia la dirección del enemigo a una dirección aleatoria.
        """
        self.direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        self.tiempo_ultimo_cambio = time.time()  # Reinicia el contador de tiempo
    
    def buscar_jugador(self, jugador_fila, jugador_columna):
        """
        Calcula la dirección hacia el jugador y la establece como dirección actual.
        jugador_fila: fila donde está el jugador
        jugador_columna: columna donde está el jugador
        """
        # Calcular diferencias de posición
        diff_fila = jugador_fila - self.fila
        diff_columna = jugador_columna - self.columna
        
        # Decidir dirección basándose en la mayor diferencia
        if abs(diff_fila) > abs(diff_columna):  # Moverse verticalmente
            if diff_fila > 0:
                self.direccion = 'abajo'
            else:
                self.direccion = 'arriba'
        else:  # Moverse horizontalmente
            if diff_columna > 0:
                self.direccion = 'derecha'
            else:
                self.direccion = 'izquierda'
    
    def actualizar(self, jugador_fila, jugador_columna):
        """
        Actualiza el comportamiento del enemigo:
        - Cada 8 segundos busca al jugador
        - Cada 1.5-3 segundos cambia de dirección aleatoriamente
        """
        tiempo_actual = time.time()
        
        # Verificar si han pasado 8 segundos para buscar al jugador
        if tiempo_actual - self.tiempo_ultima_busqueda >= 8.0:
            self.buscar_jugador(jugador_fila, jugador_columna)
            self.tiempo_ultima_busqueda = tiempo_actual
            self.buscando_jugador = True
        
        # Verificar si debe cambiar de dirección aleatoriamente
        elif tiempo_actual - self.tiempo_ultimo_cambio >= self.velocidad_cambio:
            self.cambiar_direccion_aleatoria()
            self.buscando_jugador = False
    
    def mover(self):
        """
        Mueve al enemigo una celda en su dirección actual.
        Verifica que no se salga de los límites del grid.
        """
        nueva_fila = self.fila
        nueva_columna = self.columna
        
        # Calcular nueva posición según dirección
        if self.direccion == 'arriba':
            nueva_fila -= 1
        elif self.direccion == 'abajo':
            nueva_fila += 1
        elif self.direccion == 'izquierda':
            nueva_columna -= 1
        elif self.direccion == 'derecha':
            nueva_columna += 1
        
        # Verificar que la nueva posición esté dentro del grid
        if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas:
            self.fila = nueva_fila
            self.columna = nueva_columna
        else:
            # Si choca con el borde, cambiar dirección aleatoria
            self.cambiar_direccion_aleatoria()
    
    def verificar_colision(self, jugador_fila, jugador_columna):
        """
        Verifica si el enemigo está en la misma posición que el jugador.
        Retorna True si hay colisión, False si no.
        """
        return self.fila == jugador_fila and self.columna == jugador_columna
    
    def dibujar(self):
        """
        Dibuja el enemigo en su posición del grid.
        Convierte la posición de grid (fila, columna) a píxeles (x, y).
        """
        x = self.columna * tamano_celda  # Convierte columna a posición X en píxeles
        y = self.fila * tamano_celda  # Convierte fila a posición Y en píxeles
        # Dibuja un rectángulo rojo con margen de 2 píxeles
        pygame.draw.rect(ventana, ROJO, (x+2, y+2, tamano_celda-4, tamano_celda-4))

# Función para crear enemigos (actualmente solo 1 para dificultad 1)
def crear_enemigos(dificultad):
    """
    Genera una lista de enemigos según el nivel de dificultad.
    dificultad: 1 (actualmente solo trabajamos con nivel 1 = 1 enemigo)
    Retorna una lista con objetos Enemigo en posiciones aleatorias.
    """
    enemigos = []  # Lista vacía para almacenar los enemigos
    
    # Dificultad 1: solo 1 enemigo
    cantidad = 1
    
    # Posición del jugador (centro)
    centro_fila = filas // 2
    centro_columna = columnas // 2
    
    # Crear enemigos en posiciones aleatorias
    for i in range(cantidad):
        # Generar posición aleatoria
        fila = random.randint(0, filas - 1)  # Fila aleatoria entre 0 y filas-1
        columna = random.randint(0, columnas - 1)  # Columna aleatoria entre 0 y columnas-1
        
        # Evitar que aparezcan en el centro (donde está el jugador)
        while fila == centro_fila and columna == centro_columna:
            fila = random.randint(0, filas - 1)
            columna = random.randint(0, columnas - 1)
        
        # Crear enemigo y agregarlo a la lista
        enemigos.append(Enemigo(fila, columna))
    
    return enemigos  # Devuelve la lista de enemigos creados

# Función para dibujar las líneas del grid
def dibujar_grid():
    """
    Dibuja las líneas de la cuadrícula sobre la ventana.
    Traza líneas verticales y horizontales para formar el grid.
    """
    # Dibujar líneas verticales
    for x in range(0, ancho, tamano_celda):  # Va desde 0 hasta ancho, saltando cada tamano_celda píxeles
        pygame.draw.line(ventana, GRIS, (x, 0), (x, alto), 1)  # Línea de arriba a abajo
    
    # Dibujar líneas horizontales
    for y in range(0, alto, tamano_celda):  # Va desde 0 hasta alto, saltando cada tamano_celda píxeles
        pygame.draw.line(ventana, GRIS, (0, y), (ancho, y), 1)  # Línea de izquierda a derecha

# Función para dibujar el jugador en el centro
def dibujar_jugador():
    """
    Dibuja un cuadrado azul en el centro del grid que representa al jugador.
    """
    centro_fila = filas // 2  # Calcula la fila del centro
    centro_columna = columnas // 2  # Calcula la columna del centro
    
    # Convertir posición de grid a píxeles
    x = centro_columna * tamano_celda
    y = centro_fila * tamano_celda
    
    # Dibujar rectángulo azul con margen de 2 píxeles
    pygame.draw.rect(ventana, AZUL, (x+2, y+2, tamano_celda-4, tamano_celda-4))

# Configuración inicial del juego
dificultad = 1  # Trabajando con dificultad 1 (1 enemigo)
enemigos = crear_enemigos(dificultad)  # Crear lista de enemigos

# Posición del jugador (siempre en el centro)
jugador_fila = filas // 2
jugador_columna = columnas // 2

# Variables de control del juego
juego_terminado = False  # Indica si el juego ha terminado
velocidad_movimiento = 0.3  # Enemigos se mueven cada 0.3 segundos (más lento para verlos mejor)
tiempo_ultimo_movimiento = time.time()  # Marca de tiempo del último movimiento

print(f"Juego iniciado - Dificultad {dificultad} - {len(enemigos)} enemigo(s)")
print("Sobrevive! El enemigo te busca cada 8 segundos")

# Bucle principal del juego - se ejecuta continuamente hasta que se cierre la ventana
ejecutando = True
while ejecutando:
    # Procesar todos los eventos que ocurren (clicks, teclas, cierre de ventana, etc.)
    for evento in pygame.event.get():  # Obtiene lista de todos los eventos ocurridos desde el último frame
        if evento.type == pygame.QUIT:  # Si el usuario cierra la ventana (click en X)
            ejecutando = False  # Cambia la bandera para salir del bucle
        
        # Si el juego terminó, presionar ESPACIO reinicia
        elif evento.type == pygame.KEYDOWN and juego_terminado:
            if evento.key == pygame.K_SPACE:
                # Reiniciar juego
                enemigos = crear_enemigos(dificultad)
                juego_terminado = False
                tiempo_ultimo_movimiento = time.time()
                print("Juego reiniciado")
    
    # Lógica del juego (solo si no ha terminado)
    if not juego_terminado:
        tiempo_actual = time.time()
        
        # Mover enemigos cada cierto tiempo
        if tiempo_actual - tiempo_ultimo_movimiento >= velocidad_movimiento:
            for enemigo in enemigos:
                enemigo.actualizar(jugador_fila, jugador_columna)  # Actualizar comportamiento
                enemigo.mover()  # Mover el enemigo
                
                # Verificar colisión con jugador
                if enemigo.verificar_colision(jugador_fila, jugador_columna):
                    juego_terminado = True
                    print("¡GAME OVER! Presiona ESPACIO para reiniciar")
            
            tiempo_ultimo_movimiento = tiempo_actual
    
    # Dibujar todo en la ventana
    ventana.fill(VERDE_OSCURO)  # Llena toda la ventana con el color verde oscuro
    dibujar_grid()  # Dibuja las líneas del grid
    dibujar_jugador()  # Dibuja el cuadrado azul del jugador en el centro
    
    # Dibujar todos los enemigos
    for enemigo in enemigos:  # Recorre cada enemigo en la lista
        enemigo.dibujar()  # Llama al método dibujar() de cada enemigo
    
    # Si el juego terminó, mostrar mensaje
    if juego_terminado:
        texto = fuente.render("GAME OVER", True, BLANCO)
        texto_rect = texto.get_rect(center=(ancho//2, alto//2))
        ventana.blit(texto, texto_rect)
        
        texto2 = fuente.render("ESPACIO para reiniciar", True, BLANCO)
        texto2_rect = texto2.get_rect(center=(ancho//2, alto//2 + 60))
        ventana.blit(texto2, texto2_rect)
    
    # Actualizar la pantalla para mostrar los cambios
    pygame.display.flip()  # Actualiza toda la pantalla con lo que se dibujó
    
    # Controlar la velocidad del juego
    reloj.tick(60)  # Limita el bucle a 60 iteraciones por segundo (60 FPS)

# Cerrar Pygame correctamente
pygame.quit()  # Cierra todos los módulos de Pygame
sys.exit()  # Termina el programa completamente