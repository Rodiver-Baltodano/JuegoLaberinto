import pygame
import fondo
import random
import menu

def generar_mapa_aleatorio():
    """Genera un archivo de mapa aleatorio con valores 0, 2, 3, 4"""
    GRID_COLS = 38
    GRID_ROWS = 24
    
    # Límites de elementos
    MAX_TUNELES = 4
    MAX_LIANAS = 20
    MAX_MUROS = 30
    
    # Crear mapa base lleno de caminos
    mapa = [['0' for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    
    def colocar_elemento(tipo, cantidad, tamaño):
        """Coloca elementos de un tamaño específico en el mapa"""
        colocados = 0
        intentos = 0
        max_intentos = cantidad * 50
        
        while colocados < cantidad and intentos < max_intentos:
            intentos += 1
            
            row = random.randint(0, GRID_ROWS - 1)
            col = random.randint(0, GRID_COLS - 1)
            
            if tipo == 2 and tamaño == 4:
                puede_colocar = True
                posiciones_ocupar = []
                
                if row + 2 > GRID_ROWS or col + 2 > GRID_COLS:
                    puede_colocar = False
                else:
                    for r in range(row, row + 2):
                        for c in range(col, col + 2):
                            if mapa[r][c] != '0':
                                puede_colocar = False
                                break
                            posiciones_ocupar.append((r, c))
                        if not puede_colocar:
                            break
                
                if puede_colocar:
                    for r, c in posiciones_ocupar:
                        mapa[r][c] = str(tipo)
                    colocados += 1
            
            elif tipo == 4:
                horizontal = random.choice([True, False])
                puede_colocar = True
                posiciones_ocupar = []
                
                if horizontal:
                    if row + 2 > GRID_ROWS or col + 3 > GRID_COLS:
                        puede_colocar = False
                    else:
                        for r in range(row, row + 2):
                            for c in range(col, col + 3):
                                if mapa[r][c] != '0':
                                    puede_colocar = False
                                    break
                                posiciones_ocupar.append((r, c))
                            if not puede_colocar:
                                break
                else:
                    if row + 3 > GRID_ROWS or col + 2 > GRID_COLS:
                        puede_colocar = False
                    else:
                        for r in range(row, row + 3):
                            for c in range(col, col + 2):
                                if mapa[r][c] != '0':
                                    puede_colocar = False
                                    break
                                posiciones_ocupar.append((r, c))
                            if not puede_colocar:
                                break
                
                if puede_colocar:
                    for r, c in posiciones_ocupar:
                        mapa[r][c] = str(tipo)
                    colocados += 1
            
            else:
                horizontal = random.choice([True, False])
                
                puede_colocar = True
                posiciones_ocupar = []
                
                if horizontal:
                    if col + tamaño > GRID_COLS:
                        puede_colocar = False
                    else:
                        for i in range(tamaño):
                            if mapa[row][col + i] != '0':
                                puede_colocar = False
                                break
                            posiciones_ocupar.append((row, col + i))
                else:
                    if row + tamaño > GRID_ROWS:
                        puede_colocar = False
                    else:
                        for i in range(tamaño):
                            if mapa[row + i][col] != '0':
                                puede_colocar = False
                                break
                            posiciones_ocupar.append((row + i, col))
                
                if puede_colocar:
                    for r, c in posiciones_ocupar:
                        mapa[r][c] = str(tipo)
                    colocados += 1
        
        return colocados
    
    tuneles_colocados = colocar_elemento(4, MAX_TUNELES, 6)
    lianas_colocadas = colocar_elemento(3, MAX_LIANAS, 2)
    muros_colocados = colocar_elemento(2, MAX_MUROS, 4)
    
    with open('mapa_generado.txt', 'w') as f:
        for row in mapa:
            f.write(''.join(row) + '\n')
    
    print(f"Mapa generado exitosamente:")
    print(f"  - Túneles (2 ancho x 3 largo): {tuneles_colocados}")
    print(f"  - Lianas (2 cuadrados): {lianas_colocadas}")
    print(f"  - Muros (2x2 bloques): {muros_colocados}")

class Personaje:
    def __init__(self, x, y, color, clase, es_enemigo=False, cantidadMinas=0, GRID_SIZE_X=0, GRID_SIZE_Y=0, WINDOW_WIDTH=0, WINDOW_HEIGHT=0):
        self.x = x
        self.y = y
        self.color = color
        self.GRID_SIZE_X = GRID_SIZE_X
        self.GRID_SIZE_Y = GRID_SIZE_Y
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        tamaño_jugador_x = int(GRID_SIZE_X * 0.8)
        tamaño_jugador_y = int(GRID_SIZE_Y * 0.8)
        self.image = pygame.Surface((tamaño_jugador_x, tamaño_jugador_y))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.clase = clase
        self.es_enemigo = es_enemigo
        self.cantidadMinas = cantidadMinas
        self.vivo = True
        self.tiempo_muerte = 0  # Nuevo: tiempo cuando murió
        
        if es_enemigo:
            self.velocidad_enemigo = 2
            self.direccion = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
            self.tiempo_cambio_direccion = pygame.time.get_ticks()
            self.intervalo_cambio = random.randint(1000, 3000)
            self.modo_persecucion = False
            self.tiempo_ultima_persecucion = pygame.time.get_ticks()
            self.tiempo_inicio_persecucion = 0

    def update(self, ventana):
        if self.vivo:
            self.image.fill(self.color)
            self.rect.x = self.x
            self.rect.y = self.y
            ventana.blit(self.image, self.rect)
        # Si está muerto, no se dibuja (queda oculto)
    
    def get_grid_positions(self):
        left = self.x
        right = self.x + self.image.get_width()
        top = self.y
        bottom = self.y + self.image.get_height()
        
        grid_left = left // self.GRID_SIZE_X
        grid_right = right // self.GRID_SIZE_X
        grid_top = top // self.GRID_SIZE_Y
        grid_bottom = bottom // self.GRID_SIZE_Y
        
        posiciones = []
        for grid_y in range(grid_top, grid_bottom + 1):
            for grid_x in range(grid_left, grid_right + 1):
                posiciones.append((grid_x, grid_y))
        
        return posiciones

    def colision_con_obstaculos(self, wall_group, tunel_group):
        posiciones = self.get_grid_positions()
        
        for grid_x, grid_y in posiciones:
            for muro in wall_group:
                if muro.grid_x == grid_x and muro.grid_y == grid_y:
                    if muro.bloquea_a(self):
                        return True
        
        for grid_x, grid_y in posiciones:
            for tunel in tunel_group:
                if tunel.grid_x == grid_x and tunel.grid_y == grid_y:
                    if tunel.bloquea_a(self):
                        return True
        
        return False
    
    def esta_en_liana(self, liana_group):
        posiciones = self.get_grid_positions()
        
        for grid_x, grid_y in posiciones:
            for liana in liana_group:
                if liana.grid_x == grid_x and liana.grid_y == grid_y:
                    return True
        return False
    
    def colocarMina(self, mina_group, colorMina):
        """Coloca una mina en la posición actual del personaje"""
        if self.cantidadMinas > 0:
            self.cantidadMinas -= 1
            # Obtener posición en grid
            grid_x = self.x // self.GRID_SIZE_X
            grid_y = self.y // self.GRID_SIZE_Y
            nueva_mina = Mina(grid_x, grid_y, colorMina, self.GRID_SIZE_X, self.GRID_SIZE_Y)
            mina_group.add(nueva_mina)
            return True
        return False
    
    def colisionMina(self, mina_group):
        """Verifica si el personaje colisiona con una mina"""
        if self.clase == "presa":
            return False
        else:
            posiciones = self.get_grid_positions()
            for grid_x, grid_y in posiciones:
                for mina in mina_group:
                    if mina.grid_x == grid_x and mina.grid_y == grid_y:
                        mina.kill()
                        return True
            return False
    
    def revivir(self, world_data, spawn_jugador):
        """Revive al enemigo en una nueva posición"""
        self.vivo = True
        
        # Buscar nueva posición de spawn lejos del jugador
        enemigo_spawn = None
        for row, tiles in enumerate(world_data):
            for col, tile in enumerate(tiles):
                if tile == '0':
                    dist_x = abs(col - spawn_jugador[0])
                    dist_y = abs(row - spawn_jugador[1])
                    if dist_x + dist_y > 10:
                        enemigo_spawn = (col, row)
                        break
            if enemigo_spawn:
                break
        
        if not enemigo_spawn:
            for row, tiles in enumerate(world_data):
                for col, tile in enumerate(tiles):
                    if tile == '0':
                        enemigo_spawn = (col, row)
                        break
                if enemigo_spawn:
                    break
        
        # Reposicionar enemigo
        self.x = enemigo_spawn[0] * self.GRID_SIZE_X + (self.GRID_SIZE_X - int(self.GRID_SIZE_X * 0.8)) // 2
        self.y = enemigo_spawn[1] * self.GRID_SIZE_Y + (self.GRID_SIZE_Y - int(self.GRID_SIZE_Y * 0.8)) // 2
        self.tiempo_ultima_persecucion = pygame.time.get_ticks()
    
    def mover_enemigo(self, objetivo, wall_group, tunel_group, liana_group):
        # Solo moverse si está vivo
        if not self.vivo:
            return
            
        tiempo_actual = pygame.time.get_ticks()
        
        if tiempo_actual - self.tiempo_ultima_persecucion >= 10000:
            self.modo_persecucion = True
            self.tiempo_inicio_persecucion = tiempo_actual
            self.tiempo_ultima_persecucion = tiempo_actual
        
        if self.modo_persecucion and tiempo_actual - self.tiempo_inicio_persecucion >= 3000:
            self.modo_persecucion = False
        
        velocidad_actual = self.velocidad_enemigo
        if self.esta_en_liana(liana_group):
            velocidad_actual -= 1
            if velocidad_actual < 1:
                velocidad_actual = 1
        
        pos_anterior_x = self.x
        pos_anterior_y = self.y
        
        if self.modo_persecucion:
            dx = objetivo.x - self.x
            dy = objetivo.y - self.y
            
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.x += velocidad_actual
                else:
                    self.x -= velocidad_actual
            else:
                if dy > 0:
                    self.y += velocidad_actual
                else:
                    self.y -= velocidad_actual
        else:
            if tiempo_actual - self.tiempo_cambio_direccion >= self.intervalo_cambio:
                self.direccion = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
                self.tiempo_cambio_direccion = tiempo_actual
                self.intervalo_cambio = random.randint(1000, 3000)
            
            if self.direccion == 'LEFT':
                self.x -= velocidad_actual
            elif self.direccion == 'RIGHT':
                self.x += velocidad_actual
            elif self.direccion == 'UP':
                self.y -= velocidad_actual
            elif self.direccion == 'DOWN':
                self.y += velocidad_actual
        
        if self.colision_con_obstaculos(wall_group, tunel_group):
            self.x = pos_anterior_x
            self.y = pos_anterior_y
            
            if not self.modo_persecucion:
                self.direccion = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
        
        if self.x < 0:
            self.x = 0
            self.direccion = 'RIGHT'
        if self.x + self.image.get_width() >= self.WINDOW_WIDTH:
            self.x = self.WINDOW_WIDTH - self.image.get_width()
            self.direccion = 'LEFT'
        if self.y < 0:
            self.y = 0
            self.direccion = 'DOWN'
        if self.y + self.image.get_height() >= self.WINDOW_HEIGHT:
            self.y = self.WINDOW_HEIGHT - self.image.get_height()
            self.direccion = 'UP'
    
    def colisiona_con(self, otro_personaje):
        # Solo colisiona si ambos están vivos
        if not self.vivo or not otro_personaje.vivo:
            return False
        return self.rect.colliderect(otro_personaje.rect)

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, image, GRID_SIZE_X, GRID_SIZE_Y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        
        if image:
            self.image = image.copy()
        else:
            self.image = pygame.Surface((GRID_SIZE_X, GRID_SIZE_Y), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.x = self.grid_x * GRID_SIZE_X
        self.rect.y = self.grid_y * GRID_SIZE_Y
    
    def bloquea_a(self, personaje):
        return False

class Muro(Obstaculo):
    def __init__(self, grid_x, grid_y, image, GRID_SIZE_X, GRID_SIZE_Y):
        super().__init__(grid_x, grid_y, image, GRID_SIZE_X, GRID_SIZE_Y)
        self.tipo = "muro"
    
    def bloquea_a(self, personaje):
        return True

class Liana(Obstaculo):
    def __init__(self, grid_x, grid_y, image, GRID_SIZE_X, GRID_SIZE_Y):
        super().__init__(grid_x, grid_y, image, GRID_SIZE_X, GRID_SIZE_Y)
        self.tipo = "liana"
    
    def bloquea_a(self, personaje):
        return False
    
    def ralentiza_a(self, personaje):
        return True

class Tunel(Obstaculo):
    def __init__(self, grid_x, grid_y, image, GRID_SIZE_X, GRID_SIZE_Y):
        super().__init__(grid_x, grid_y, image, GRID_SIZE_X, GRID_SIZE_Y)
        self.tipo = "tunel"
    
    def bloquea_a(self, personaje):
        return personaje.clase != "presa"

class Mina(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, color, GRID_SIZE_X, GRID_SIZE_Y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.color = color
        self.image = pygame.Surface((GRID_SIZE_X, GRID_SIZE_Y))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.grid_x * GRID_SIZE_X
        self.rect.y = self.grid_y * GRID_SIZE_Y

def iniciar_juego():
    """Función principal que inicia el juego y maneja el bucle del menú"""
    pygame.init()
    
    while True:  # Bucle principal del menú
        # Mostrar menú y obtener selección
        modo_seleccionado = menu.funcionMenu()
        
        # Si el usuario cierra el menú, salir del juego
        if modo_seleccionado is None:
            break
        
        # Si selecciona modo cazador (aún no implementado), volver al menú
        if modo_seleccionado == "cazador":
            print("Modo Cazador aún no está implementado")
            continue  # Volver al menú
        
        print(f"Modo seleccionado: {modo_seleccionado}")
        
        # Generar nuevo mapa
        generar_mapa_aleatorio()
        
        # Configuración de la ventana
        full_map_scaled, WINDOW_WIDTH, WINDOW_HEIGHT, GRID_COLS, GRID_ROWS, GRID_SIZE_X, GRID_SIZE_Y = fondo.iniciar_fondo()
        
        ventana = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Laberinto con Fondo")
        
        # Colores
        colorJugador = (255, 255, 255)
        colorEnemigo = (255, 0, 0)
        colorMina = (255, 165, 0)
        
        # Cargar imágenes
        try:
            liana_image = pygame.image.load("imagenes/liana.png")
            liana_image = pygame.transform.scale(liana_image, (GRID_SIZE_X, GRID_SIZE_Y))
        except pygame.error as e:
            print(f"No se pudo cargar la imagen de liana: {e}")
            liana_image = None
        
        try:
            muro_image = pygame.image.load("imagenes/muro.png")
            muro_image = pygame.transform.scale(muro_image, (GRID_SIZE_X, GRID_SIZE_Y))
        except pygame.error as e:
            print(f"No se pudo cargar la imagen de muro: {e}")
            muro_image = None
        
        try:
            tunel_image = pygame.image.load("imagenes/tunel.png")
            tunel_image = pygame.transform.scale(tunel_image, (GRID_SIZE_X, GRID_SIZE_Y))
        except pygame.error as e:
            print(f"No se pudo cargar la imagen de tunel: {e}")
            tunel_image = None
        
        # Variables del juego
        velocidad = 3
        Puntuacion = 0
        
        # Variables de tiempo
        TIEMPO_LIMITE = 120000  # 2 minutos en milisegundos
        tiempo_inicio = pygame.time.get_ticks()
        # Variables de pausa y puntuación
        juego_pausado = False
        tiempo_pausa_inicio = 0
        tiempo_total_pausado = 0
        ultimo_segundo_puntuacion = 0
        # Variables de stamina
        stamina_max = 100
        stamina_actual = 100
        regeneracion_stamina = 0.5
        consumo_stamina = 2
        
        wall_group = pygame.sprite.Group()
        liana_group = pygame.sprite.Group()
        tunel_group = pygame.sprite.Group()
        mina_group = pygame.sprite.Group()
        
        reloj = pygame.time.Clock()
        
        # Leer mapa
        world_data = []
        spawn_position = (1, 1)
        
        with open('mapa_generado.txt', 'r') as world:
            for line in world:
                world_data.append(line.strip())
        
        # Crear obstáculos
        for row, tiles in enumerate(world_data):
            for col, tile in enumerate(tiles):
                if tile == '2':
                    muro = Muro(col, row, muro_image, GRID_SIZE_X, GRID_SIZE_Y)
                    wall_group.add(muro)
                elif tile == '3':
                    liana = Liana(col, row, liana_image, GRID_SIZE_X, GRID_SIZE_Y)
                    liana_group.add(liana)
                elif tile == '4':
                    tunel = Tunel(col, row, tunel_image, GRID_SIZE_X, GRID_SIZE_Y)
                    tunel_group.add(tunel)
        
        # Buscar posición de spawn
        for row, tiles in enumerate(world_data):
            for col, tile in enumerate(tiles):
                if tile == '0':
                    spawn_position = (col, row)
                    break
            if spawn_position != (1, 1):
                break
        
        # Crear jugador
        spawn_x_pixel = spawn_position[0] * GRID_SIZE_X + (GRID_SIZE_X - int(GRID_SIZE_X * 0.8)) // 2
        spawn_y_pixel = spawn_position[1] * GRID_SIZE_Y + (GRID_SIZE_Y - int(GRID_SIZE_Y * 0.8)) // 2
        jugador = Personaje(spawn_x_pixel, spawn_y_pixel, colorJugador, clase="presa", 
                           cantidadMinas=3,
                           GRID_SIZE_X=GRID_SIZE_X, GRID_SIZE_Y=GRID_SIZE_Y,
                           WINDOW_WIDTH=WINDOW_WIDTH, WINDOW_HEIGHT=WINDOW_HEIGHT)
        
        # Crear lista de enemigos (6 enemigos)
        enemigos = []
        NUM_ENEMIGOS = 6
        
        for i in range(NUM_ENEMIGOS):
            # Buscar posición para cada enemigo
            enemigo_spawn = None
            intentos = 0
            max_intentos = 100
            
            while not enemigo_spawn and intentos < max_intentos:
                intentos += 1
                for row, tiles in enumerate(world_data):
                    for col, tile in enumerate(tiles):
                        if tile == '0':
                            # Verificar distancia con jugador
                            dist_x = abs(col - spawn_position[0])
                            dist_y = abs(row - spawn_position[1])
                            
                            # Verificar distancia con otros enemigos ya creados
                            muy_cerca_de_otros = False
                            for otro_enemigo in enemigos:
                                otro_grid_x = otro_enemigo.x // GRID_SIZE_X
                                otro_grid_y = otro_enemigo.y // GRID_SIZE_Y
                                dist_otro_x = abs(col - otro_grid_x)
                                dist_otro_y = abs(row - otro_grid_y)
                                if dist_otro_x + dist_otro_y < 5:  # Mínimo 5 casillas entre enemigos
                                    muy_cerca_de_otros = True
                                    break
                            
                            if dist_x + dist_y > 8 and not muy_cerca_de_otros:
                                enemigo_spawn = (col, row)
                                break
                    if enemigo_spawn:
                        break
            
            # Si no se encontró posición ideal, buscar cualquier posición válida
            if not enemigo_spawn:
                for row, tiles in enumerate(world_data):
                    for col, tile in enumerate(tiles):
                        if tile == '0' and (col, row) != spawn_position:
                            enemigo_spawn = (col, row)
                            break
                    if enemigo_spawn:
                        break
            
            # Crear enemigo en la posición encontrada
            if enemigo_spawn:
                enemigo_x_pixel = enemigo_spawn[0] * GRID_SIZE_X + (GRID_SIZE_X - int(GRID_SIZE_X * 0.8)) // 2
                enemigo_y_pixel = enemigo_spawn[1] * GRID_SIZE_Y + (GRID_SIZE_Y - int(GRID_SIZE_Y * 0.8)) // 2
                nuevo_enemigo = Personaje(enemigo_x_pixel, enemigo_y_pixel, colorEnemigo, clase="cazador", es_enemigo=True,
                                   cantidadMinas=0,
                                   GRID_SIZE_X=GRID_SIZE_X, GRID_SIZE_Y=GRID_SIZE_Y,
                                   WINDOW_WIDTH=WINDOW_WIDTH, WINDOW_HEIGHT=WINDOW_HEIGHT)
                enemigos.append(nuevo_enemigo)
        
        def dibujar_grid():
            GRIS = (100, 100, 100)
            
            for x in range(0, WINDOW_WIDTH, GRID_SIZE_X):
                pygame.draw.line(ventana, GRIS, (x, 0), (x, WINDOW_HEIGHT), 1)
            
            for y in range(0, WINDOW_HEIGHT, GRID_SIZE_Y):
                pygame.draw.line(ventana, GRIS, (0, y), (WINDOW_WIDTH, y), 1)
        
        def movimiento():
            nonlocal stamina_actual
            key = pygame.key.get_pressed()
            
            # Verificar si está corriendo
            corriendo = (key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]) and stamina_actual > 0
            
            if corriendo:
                velocidad_actual = velocidad * 2
                stamina_actual -= consumo_stamina
                stamina_actual = max(0, stamina_actual)
            else:
                velocidad_actual = velocidad
            
            # Aplicar ralentización por lianas
            if jugador.esta_en_liana(liana_group):
                velocidad_actual = max(1, velocidad_actual - 1)
            
            pos_anterior_x = jugador.x
            pos_anterior_y = jugador.y
            
            # Movimiento con flechas
            if key[pygame.K_LEFT]:
                jugador.x -= velocidad_actual
                if jugador.x < 0:
                    jugador.x = 0
                elif jugador.colision_con_obstaculos(wall_group, tunel_group):
                    jugador.x = pos_anterior_x
            
            elif key[pygame.K_RIGHT]:
                jugador.x += velocidad_actual
                if jugador.x + jugador.image.get_width() >= WINDOW_WIDTH:
                    jugador.x = WINDOW_WIDTH - jugador.image.get_width()
                elif jugador.colision_con_obstaculos(wall_group, tunel_group):
                    jugador.x = pos_anterior_x
            
            elif key[pygame.K_UP]:
                jugador.y -= velocidad_actual
                if jugador.y < 0:
                    jugador.y = 0
                elif jugador.colision_con_obstaculos(wall_group, tunel_group):
                    jugador.y = pos_anterior_y
            
            elif key[pygame.K_DOWN]:
                jugador.y += velocidad_actual
                if jugador.y + jugador.image.get_height() >= WINDOW_HEIGHT:
                    jugador.y = WINDOW_HEIGHT - jugador.image.get_height()
                elif jugador.colision_con_obstaculos(wall_group, tunel_group):
                    jugador.y = pos_anterior_y
            
            # Movimiento con WASD
            elif key[pygame.K_a]:
                jugador.x -= velocidad_actual
                if jugador.x < 0:
                    jugador.x = 0
                elif jugador.colision_con_obstaculos(wall_group, tunel_group):
                    jugador.x = pos_anterior_x
            
            elif key[pygame.K_d]:
                jugador.x += velocidad_actual
                if jugador.x + jugador.image.get_width() >= WINDOW_WIDTH:
                    jugador.x = WINDOW_WIDTH - jugador.image.get_width()
                elif jugador.colision_con_obstaculos(wall_group, tunel_group):
                    jugador.x = pos_anterior_x
            
            elif key[pygame.K_w]:
                jugador.y -= velocidad_actual
                if jugador.y < 0:
                    jugador.y = 0
                elif jugador.colision_con_obstaculos(wall_group, tunel_group):
                    jugador.y = pos_anterior_y
            
            elif key[pygame.K_s]:
                jugador.y += velocidad_actual
                if jugador.y + jugador.image.get_height() >= WINDOW_HEIGHT:
                    jugador.y = WINDOW_HEIGHT - jugador.image.get_height()
                elif jugador.colision_con_obstaculos(wall_group, tunel_group):
                    jugador.y = pos_anterior_y
        
        # Bucle principal del juego
        ejecutando = True
        mostrar_grid = False
        juego_terminado = False
        victoria = False
        volver_menu = False
        
        pygame.font.init()
        fuente_grande = pygame.font.Font(None, 74)
        fuente_mediana = pygame.font.Font(None, 36)
        fuente_pequena = pygame.font.Font(None, 24)
        
        while ejecutando:
            if full_map_scaled:
                ventana.blit(full_map_scaled, (0, 0))
            
            wall_group.draw(ventana)
            liana_group.draw(ventana)
            tunel_group.draw(ventana)
            mina_group.draw(ventana)
            
            if not juego_terminado and not juego_pausado:
                # Calcular tiempo restante
                tiempo_actual = pygame.time.get_ticks()
                tiempo_transcurrido = tiempo_actual - tiempo_inicio - tiempo_total_pausado  # MODIFICAR
                tiempo_restante = max(0, TIEMPO_LIMITE - tiempo_transcurrido)
                
                # Verificar si se acabó el tiempo - VICTORIA
                if tiempo_restante <= 0:
                    juego_terminado = True
                    victoria = True
                
                movimiento()
                
                # Mover todos los enemigos
                for enemigo in enemigos:
                    enemigo.mover_enemigo(jugador, wall_group, tunel_group, liana_group)
                
                # Verificar colisión de cada enemigo con minas
                for enemigo in enemigos:
                    if enemigo.colisionMina(mina_group):
                        jugador.cantidadMinas += 1
                        enemigo.vivo = False
                        enemigo.tiempo_muerte = tiempo_actual
                        Puntuacion += 10
                
                # Verificar si los enemigos deben revivir
                for enemigo in enemigos:
                    if not enemigo.vivo and (tiempo_actual - enemigo.tiempo_muerte >= 10000):
                        enemigo.revivir(world_data, spawn_position)
                
                # Verificar colisión jugador con cualquier enemigo
                for enemigo in enemigos:
                    if jugador.colisiona_con(enemigo) and enemigo.vivo:
                        juego_terminado = True
                        victoria = False
                        break
                
            # Incrementar puntuación (1 punto por segundo)
            segundo_actual = tiempo_transcurrido // 1000
            if segundo_actual > ultimo_segundo_puntuacion:
                Puntuacion += 1
                ultimo_segundo_puntuacion = segundo_actual
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    import sys
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        ejecutando = False
                        volver_menu = False
                    elif evento.key == pygame.K_g:
                        mostrar_grid = not mostrar_grid
                    elif evento.key == pygame.K_p and not juego_terminado:  # AGREGAR
                        juego_pausado = not juego_pausado
                        if juego_pausado:
                            tiempo_pausa_inicio = pygame.time.get_ticks()
                        else:
                            tiempo_total_pausado += pygame.time.get_ticks() - tiempo_pausa_inicio
                    elif evento.key == pygame.K_SPACE and not juego_terminado:
                        jugador.colocarMina(mina_group, colorMina)
                    elif evento.key == pygame.K_r and juego_terminado:
                        # Reiniciar juego
                        juego_terminado = False
                        victoria = False
                        Puntuacion = 0
                        stamina_actual = stamina_max
                        tiempo_inicio = pygame.time.get_ticks()  # Reiniciar temporizador
                        juego_pausado = False
                        tiempo_pausa_inicio = 0
                        tiempo_total_pausado = 0

                        # Regenerar mapa
                        generar_mapa_aleatorio()
                        wall_group.empty()
                        liana_group.empty()
                        tunel_group.empty()
                        mina_group.empty()
                        
                        # Leer nuevo mapa
                        world_data = []
                        with open('mapa_generado.txt', 'r') as world:
                            for line in world:
                                world_data.append(line.strip())
                        
                        # Recrear obstáculos
                        for row, tiles in enumerate(world_data):
                            for col, tile in enumerate(tiles):
                                if tile == '2':
                                    muro = Muro(col, row, muro_image, GRID_SIZE_X, GRID_SIZE_Y)
                                    wall_group.add(muro)
                                elif tile == '3':
                                    liana = Liana(col, row, liana_image, GRID_SIZE_X, GRID_SIZE_Y)
                                    liana_group.add(liana)
                                elif tile == '4':
                                    tunel = Tunel(col, row, tunel_image, GRID_SIZE_X, GRID_SIZE_Y)
                                    tunel_group.add(tunel)
                        
                        # Buscar nuevo spawn
                        spawn_position = (1, 1)
                        for row, tiles in enumerate(world_data):
                            for col, tile in enumerate(tiles):
                                if tile == '0':
                                    spawn_position = (col, row)
                                    break
                            if spawn_position != (1, 1):
                                break
                        
                        # Reiniciar jugador
                        spawn_x_pixel = spawn_position[0] * GRID_SIZE_X + (GRID_SIZE_X - int(GRID_SIZE_X * 0.8)) // 2
                        spawn_y_pixel = spawn_position[1] * GRID_SIZE_Y + (GRID_SIZE_Y - int(GRID_SIZE_Y * 0.8)) // 2
                        jugador.x = spawn_x_pixel
                        jugador.y = spawn_y_pixel
                        # En el bloque de reinicio con 'R'
                        juego_pausado = False
                        tiempo_total_pausado = 0
                        jugador.cantidadMinas = 3
                        jugador.vivo = True
                        
                        # Buscar spawn enemigo
                        # Reiniciar enemigos
                        enemigos.clear()
                        for i in range(NUM_ENEMIGOS):
                            enemigo_spawn = None
                            intentos = 0
                            max_intentos = 100
                            
                            while not enemigo_spawn and intentos < max_intentos:
                                intentos += 1
                                for row, tiles in enumerate(world_data):
                                    for col, tile in enumerate(tiles):
                                        if tile == '0':
                                            dist_x = abs(col - spawn_position[0])
                                            dist_y = abs(row - spawn_position[1])
                                            
                                            muy_cerca_de_otros = False
                                            for otro_enemigo in enemigos:
                                                otro_grid_x = otro_enemigo.x // GRID_SIZE_X
                                                otro_grid_y = otro_enemigo.y // GRID_SIZE_Y
                                                dist_otro_x = abs(col - otro_grid_x)
                                                dist_otro_y = abs(row - otro_grid_y)
                                                if dist_otro_x + dist_otro_y < 5:
                                                    muy_cerca_de_otros = True
                                                    break
                                            
                                            if dist_x + dist_y > 8 and not muy_cerca_de_otros:
                                                enemigo_spawn = (col, row)
                                                break
                                    if enemigo_spawn:
                                        break
                            
                            if not enemigo_spawn:
                                for row, tiles in enumerate(world_data):
                                    for col, tile in enumerate(tiles):
                                        if tile == '0' and (col, row) != spawn_position:
                                            enemigo_spawn = (col, row)
                                            break
                                    if enemigo_spawn:
                                        break
                            
                            if enemigo_spawn:
                                enemigo_x_pixel = enemigo_spawn[0] * GRID_SIZE_X + (GRID_SIZE_X - int(GRID_SIZE_X * 0.8)) // 2
                                enemigo_y_pixel = enemigo_spawn[1] * GRID_SIZE_Y + (GRID_SIZE_Y - int(GRID_SIZE_Y * 0.8)) // 2
                                nuevo_enemigo = Personaje(enemigo_x_pixel, enemigo_y_pixel, colorEnemigo, clase="cazador", es_enemigo=True,
                                           cantidadMinas=0,
                                           GRID_SIZE_X=GRID_SIZE_X, GRID_SIZE_Y=GRID_SIZE_Y,
                                           WINDOW_WIDTH=WINDOW_WIDTH, WINDOW_HEIGHT=WINDOW_HEIGHT)
                                nuevo_enemigo.tiempo_ultima_persecucion = pygame.time.get_ticks()
                                enemigos.append(nuevo_enemigo)
                        
                    elif evento.key == pygame.K_m and juego_terminado:
                        ejecutando = False
                        volver_menu = True
            
            # Regenerar stamina si no está corriendo
            key = pygame.key.get_pressed()
            if not (key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]):
                stamina_actual = min(stamina_max, stamina_actual + regeneracion_stamina)
            
            # Dibujar interfaz superior (puntuación y tiempo)
            panel_alto = 60
            panel = pygame.Surface((WINDOW_WIDTH, panel_alto))
            panel.set_alpha(180)
            panel.fill((0, 0, 0))
            ventana.blit(panel, (0, 0))
            
            # Mostrar puntuación
            texto_puntuacion = fuente_mediana.render(f"Puntuacion: {Puntuacion}", True, (255, 255, 255))
            ventana.blit(texto_puntuacion, (20, 15))
            
            # Mostrar tiempo restante
            if not juego_terminado:
                tiempo_actual = pygame.time.get_ticks()
                tiempo_transcurrido = tiempo_actual - tiempo_inicio
                tiempo_restante = max(0, TIEMPO_LIMITE - tiempo_transcurrido)
                segundos_restantes = tiempo_restante // 1000
                minutos = segundos_restantes // 60
                segundos = segundos_restantes % 60
                
                color_tiempo = (255, 255, 255)
                if tiempo_restante < 30000:  # Menos de 30 segundos
                    color_tiempo = (255, 0, 0)
                elif tiempo_restante < 60000:  # Menos de 1 minuto
                    color_tiempo = (255, 255, 0)
                
                texto_tiempo = fuente_mediana.render(f"Tiempo: {minutos:02d}:{segundos:02d}", True, color_tiempo)
                ventana.blit(texto_tiempo, (WINDOW_WIDTH - 220, 15))
            
            # Dibujar barra de stamina (más abajo para no interferir con el panel)
            barra_ancho = 200
            barra_alto = 20
            barra_x = 20
            barra_y = 70
            pygame.draw.rect(ventana, (100, 100, 100), (barra_x, barra_y, barra_ancho, barra_alto))
            barra_actual_ancho = (stamina_actual / stamina_max) * barra_ancho
            pygame.draw.rect(ventana, (0, 255, 0), (barra_x, barra_y, barra_actual_ancho, barra_alto))
            
            # Mostrar cantidad de minas
            texto_minas = fuente_pequena.render(f"Minas: {jugador.cantidadMinas}", True, (255, 255, 255))
            ventana.blit(texto_minas, (20, 100))
            
            if mostrar_grid:
                dibujar_grid()
            
            jugador.update(ventana)
            for enemigo in enemigos:
                enemigo.update(ventana)
            
            if juego_terminado:
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                ventana.blit(overlay, (0, 0))
                
                if victoria:
                    texto_resultado = fuente_grande.render("¡VICTORIA!", True, (0, 255, 0))
                    texto_mensaje = fuente_mediana.render("¡Sobreviviste 2 minutos!", True, (255, 255, 255))
                else:
                    texto_resultado = fuente_grande.render("GAME OVER", True, (255, 0, 0))
                    texto_mensaje = fuente_mediana.render("El enemigo te atrapó", True, (255, 255, 255))
                
                texto_puntuacion = fuente_mediana.render(f"Puntuacion: {Puntuacion}", True, (255, 255, 255))
                texto_reiniciar = fuente_mediana.render("Presiona R para reiniciar", True, (255, 255, 255))
                texto_menu = fuente_mediana.render("Presiona M para volver al menu", True, (255, 255, 255))
                
                rect_resultado = texto_resultado.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
                rect_mensaje = texto_mensaje.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
                rect_puntuacion = texto_puntuacion.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
                rect_reiniciar = texto_reiniciar.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
                rect_menu = texto_menu.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 130))
                
                ventana.blit(texto_resultado, rect_resultado)
                ventana.blit(texto_mensaje, rect_mensaje)
                ventana.blit(texto_puntuacion, rect_puntuacion)
                ventana.blit(texto_reiniciar, rect_reiniciar)
                ventana.blit(texto_menu, rect_menu)
            
            # Mostrar pantalla de pausa
            if juego_pausado and not juego_terminado:
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                overlay.set_alpha(200)
                overlay.fill((0, 0, 0))
                ventana.blit(overlay, (0, 0))
                
                texto_pausa = fuente_grande.render("PAUSA", True, (255, 255, 255))
                texto_continuar = fuente_mediana.render("Presiona P para continuar", True, (255, 255, 255))
                
                rect_pausa = texto_pausa.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
                rect_continuar = texto_continuar.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
                
                ventana.blit(texto_pausa, rect_pausa)
                ventana.blit(texto_continuar, rect_continuar)

            pygame.display.flip()
            reloj.tick(60)
        
        # Si no se quiere volver al menú, salir del bucle principal
        if not volver_menu:
            pygame.quit()
            import sys
            sys.exit()
            break

if __name__ == "__main__": 
    iniciar_juego()
