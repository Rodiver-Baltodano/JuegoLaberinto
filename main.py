import pygame
import fondo
import random
import menu  # Importar el módulo del menú

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
    def __init__(self, x, y, color, clase, es_enemigo=False, GRID_SIZE_X=0, GRID_SIZE_Y=0, WINDOW_WIDTH=0, WINDOW_HEIGHT=0):
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
        
        if es_enemigo:
            self.velocidad_enemigo = 2
            self.direccion = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
            self.tiempo_cambio_direccion = pygame.time.get_ticks()
            self.intervalo_cambio = random.randint(1000, 3000)
            self.modo_persecucion = False
            self.tiempo_ultima_persecucion = pygame.time.get_ticks()
            self.tiempo_inicio_persecucion = 0

    def update(self, ventana):
        self.image.fill(self.color)
        self.rect.x = self.x
        self.rect.y = self.y
        ventana.blit(self.image, self.rect)
    
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
    
    def mover_enemigo(self, objetivo, wall_group, tunel_group, liana_group):
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
        
        # Cargar imágenes
        try:
            liana_image = pygame.image.load("liana.png")
            liana_image = pygame.transform.scale(liana_image, (GRID_SIZE_X, GRID_SIZE_Y))
        except pygame.error as e:
            print(f"No se pudo cargar la imagen de liana: {e}")
            liana_image = None
        
        try:
            muro_image = pygame.image.load("muro.png")
            muro_image = pygame.transform.scale(muro_image, (GRID_SIZE_X, GRID_SIZE_Y))
        except pygame.error as e:
            print(f"No se pudo cargar la imagen de muro: {e}")
            muro_image = None
        
        try:
            tunel_image = pygame.image.load("tunel.png")
            tunel_image = pygame.transform.scale(tunel_image, (GRID_SIZE_X, GRID_SIZE_Y))
        except pygame.error as e:
            print(f"No se pudo cargar la imagen de tunel: {e}")
            tunel_image = None
        
        velocidad = 3
        
        wall_group = pygame.sprite.Group()
        liana_group = pygame.sprite.Group()
        tunel_group = pygame.sprite.Group()
        
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
                           GRID_SIZE_X=GRID_SIZE_X, GRID_SIZE_Y=GRID_SIZE_Y,
                           WINDOW_WIDTH=WINDOW_WIDTH, WINDOW_HEIGHT=WINDOW_HEIGHT)
        
        # Buscar posición para enemigo
        enemigo_spawn = None
        for row, tiles in enumerate(world_data):
            for col, tile in enumerate(tiles):
                if tile == '0':
                    dist_x = abs(col - spawn_position[0])
                    dist_y = abs(row - spawn_position[1])
                    if dist_x + dist_y > 10:
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
        
        # Crear enemigo
        enemigo_x_pixel = enemigo_spawn[0] * GRID_SIZE_X + (GRID_SIZE_X - int(GRID_SIZE_X * 0.8)) // 2
        enemigo_y_pixel = enemigo_spawn[1] * GRID_SIZE_Y + (GRID_SIZE_Y - int(GRID_SIZE_Y * 0.8)) // 2
        enemigo = Personaje(enemigo_x_pixel, enemigo_y_pixel, colorEnemigo, clase="cazador", es_enemigo=True,
                           GRID_SIZE_X=GRID_SIZE_X, GRID_SIZE_Y=GRID_SIZE_Y,
                           WINDOW_WIDTH=WINDOW_WIDTH, WINDOW_HEIGHT=WINDOW_HEIGHT)
        
        def dibujar_grid():
            GRIS = (100, 100, 100)
            
            for x in range(0, WINDOW_WIDTH, GRID_SIZE_X):
                pygame.draw.line(ventana, GRIS, (x, 0), (x, WINDOW_HEIGHT), 1)
            
            for y in range(0, WINDOW_HEIGHT, GRID_SIZE_Y):
                pygame.draw.line(ventana, GRIS, (0, y), (WINDOW_WIDTH, y), 1)
        
        def movimiento():
            key = pygame.key.get_pressed()
            
            velocidad_actual = velocidad
            if jugador.esta_en_liana(liana_group):
                velocidad_actual -= 1
                if velocidad_actual < 1:
                    velocidad_actual = 1
            
            pos_anterior_x = jugador.x
            pos_anterior_y = jugador.y
            
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
        
        # Bucle principal del juego
        ejecutando = True
        mostrar_grid = False
        juego_terminado = False
        volver_menu = False
        
        pygame.font.init()
        fuente_grande = pygame.font.Font(None, 74)
        fuente_mediana = pygame.font.Font(None, 36)
        
        while ejecutando:
            if full_map_scaled:
                ventana.blit(full_map_scaled, (0, 0))
            
            wall_group.draw(ventana)
            liana_group.draw(ventana)
            tunel_group.draw(ventana)
            
            if not juego_terminado:
                movimiento()
                enemigo.mover_enemigo(jugador, wall_group, tunel_group, liana_group)
                
                if jugador.colisiona_con(enemigo):
                    juego_terminado = True
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    import sys
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        ejecutando = False
                        volver_menu = False  # Salir completamente
                    elif evento.key == pygame.K_g:
                        mostrar_grid = not mostrar_grid
                    elif evento.key == pygame.K_r and juego_terminado:
                        juego_terminado = False
                        jugador.x = spawn_x_pixel
                        jugador.y = spawn_y_pixel
                        enemigo.x = enemigo_x_pixel
                        enemigo.y = enemigo_y_pixel
                        enemigo.tiempo_ultima_persecucion = pygame.time.get_ticks()
                    elif evento.key == pygame.K_m and juego_terminado:
                        # Volver al menú
                        ejecutando = False
                        volver_menu = True
            
            if mostrar_grid:
                dibujar_grid()
            
            jugador.update(ventana)
            enemigo.update(ventana)
            
            if juego_terminado:
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                ventana.blit(overlay, (0, 0))
                
                texto_game_over = fuente_grande.render("GAME OVER", True, (255, 0, 0))
                texto_reiniciar = fuente_mediana.render("Presiona R para reiniciar", True, (255, 255, 255))
                texto_menu = fuente_mediana.render("Presiona M para volver al menu", True, (255, 255, 255))
                
                rect_game_over = texto_game_over.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
                rect_reiniciar = texto_reiniciar.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
                rect_menu = texto_menu.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70))
                
                ventana.blit(texto_game_over, rect_game_over)
                ventana.blit(texto_reiniciar, rect_reiniciar)
                ventana.blit(texto_menu, rect_menu)
            
            pygame.display.flip()
            reloj.tick(60)
        
        # Si no se quiere volver al menú, salir del bucle principal
        if not volver_menu:
            break
    
    pygame.quit()
    import sys
    sys.exit()

# Ejecutar el juego
if __name__ == "__main__":
    iniciar_juego()