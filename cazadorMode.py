import pygame
import sys
import random
import JuegoLaberinto.fondo as fondo
import salonFama as salonFama
from JuegoLaberinto.ventanaRegistro import nombre_jugador
from JuegoLaberinto.presaMode import Personaje, Obstaculo, Muro, Liana, Tunel, generar_mapa_aleatorio

def menu_dificultad():
    """
    Muestra el menú de selección de dificultad.
    Retorna: 'facil' o 'dificil' según la selección del jugador, o None si cierra
    """
    if not pygame.get_init():
        pygame.init()
    
    ANCHO = 650
    ALTO = 450
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Seleccionar Dificultad")
    
    try:
        fondo_img = pygame.image.load("imagenes/fondoMenu.png")
        fondo_img = pygame.transform.scale(fondo_img, (ANCHO, ALTO))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
        fondo_img = pygame.Surface((ANCHO, ALTO))
        fondo_img.fill((135, 206, 235))
    
    fuente_titulo = pygame.font.Font(None, 60)
    fuente_botones = pygame.font.Font(None, 48)
    
    class Boton:
        def __init__(self, texto, x, y, ancho, alto):
            self.texto = texto
            self.rect = pygame.Rect(x, y, ancho, alto)
            self.color_normal = (60, 60, 60)
            self.color_hover = (80, 80, 80)
            self.color_actual = self.color_normal
            self.border_radius = 7
            self.opacidad = int(255 * 0.85)
            
        def dibujar(self, superficie):
            superficie_boton = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            color_con_alpha = (*self.color_actual, self.opacidad)
            pygame.draw.rect(superficie_boton, color_con_alpha, superficie_boton.get_rect(), border_radius=self.border_radius)
            
            texto_render = fuente_botones.render(self.texto, True, (255, 255, 255))
            texto_rect = texto_render.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
            superficie_boton.blit(texto_render, texto_rect)
            superficie.blit(superficie_boton, self.rect.topleft)
        
        def verificar_hover(self, pos_mouse):
            if self.rect.collidepoint(pos_mouse):
                self.color_actual = self.color_hover
                return True
            else:
                self.color_actual = self.color_normal
                return False
        
        def verificar_click(self, pos_mouse):
            return self.rect.collidepoint(pos_mouse)
    
    padding = 10
    ancho_texto_boton = 230
    alto_texto_boton = 40
    ancho_boton = ancho_texto_boton + (padding * 2)
    alto_boton = alto_texto_boton + (padding * 2)
    x_centrado = (ANCHO - ancho_boton) // 2
    y_primer_boton = 180
    
    boton_facil = Boton("Modo Fácil", x_centrado, y_primer_boton, ancho_boton, alto_boton)
    boton_dificil = Boton("Modo Difícil", x_centrado, y_primer_boton + alto_boton + 30, ancho_boton, alto_boton)
    
    reloj = pygame.time.Clock()
    seleccion = None
    ejecutando = True
    
    while ejecutando:
        pos_mouse = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return None
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_facil.verificar_click(pos_mouse):
                    seleccion = "facil"
                    ejecutando = False
                elif boton_dificil.verificar_click(pos_mouse):
                    seleccion = "dificil"
                    ejecutando = False
        
        boton_facil.verificar_hover(pos_mouse)
        boton_dificil.verificar_hover(pos_mouse)
        
        ventana.blit(fondo_img, (0, 0))
        
        texto_titulo = "Selecciona Dificultad"
        ancho_texto, alto_texto = fuente_titulo.size(texto_titulo)
        x_titulo = (ANCHO - ancho_texto) // 2
        y_titulo = 40
        
        superficie_fondo_titulo = pygame.Surface((ANCHO, alto_texto + 20))
        superficie_fondo_titulo.set_alpha(int(255 * 0.7))
        superficie_fondo_titulo.fill((40, 40, 40))
        ventana.blit(superficie_fondo_titulo, (0, y_titulo - 10))
        
        texto_borde = fuente_titulo.render(texto_titulo, True, (0, 0, 0))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ventana.blit(texto_borde, (x_titulo + dx * 0.45, y_titulo + dy * 0.45))
        
        texto_superficie = fuente_titulo.render(texto_titulo, True, (255, 255, 255))
        ventana.blit(texto_superficie, (x_titulo, y_titulo))
        
        boton_facil.dibujar(ventana)
        boton_dificil.dibujar(ventana)
        
        pygame.display.flip()
        reloj.tick(60)
    
    return seleccion

class ZonaSegura(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, GRID_SIZE_X, GRID_SIZE_Y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.image = pygame.Surface((GRID_SIZE_X * 3, GRID_SIZE_Y * 3))
        self.image.set_alpha(150)
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE_X
        self.rect.y = grid_y * GRID_SIZE_Y

def iniciar_modo_cazador(jugador_nombre="Jugador"):
    pygame.init()
    
    while True:
        dificultad = menu_dificultad()
        
        if dificultad is None:
            return "menu"
        
        print(f"Dificultad seleccionada: {dificultad}")
        
        # Configuración según dificultad
        if dificultad == "facil":
            NUM_PRESAS = 3
            TIEMPO_LIMITE = 120000  # 2 minutos
            INTERVALO_BUSQUEDA = 7000  # 7 segundos
            MULTIPLICADOR = 1
        else:  # difícil
            NUM_PRESAS = 10
            TIEMPO_LIMITE = 60000  # 1 minuto
            INTERVALO_BUSQUEDA = 5000  # 5 segundos
            MULTIPLICADOR = 2
        
        DURACION_BUSQUEDA = 3000  # 3 segundos
        
        generar_mapa_aleatorio()
        
        full_map_scaled, WINDOW_WIDTH, WINDOW_HEIGHT, GRID_COLS, GRID_ROWS, GRID_SIZE_X, GRID_SIZE_Y = fondo.iniciar_fondo()
        
        ventana = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Modo Cazador")
        
        colorJugador = (255, 0, 0)  # Rojo para cazador
        colorPresa = (255, 255, 255)  # Blanco para presas
        
        try:
            liana_image = pygame.image.load("imagenes/liana.png")
            liana_image = pygame.transform.scale(liana_image, (GRID_SIZE_X, GRID_SIZE_Y))
        except:
            liana_image = None
        
        try:
            muro_image = pygame.image.load("imagenes/muro.png")
            muro_image = pygame.transform.scale(muro_image, (GRID_SIZE_X, GRID_SIZE_Y))
        except:
            muro_image = None
        
        try:
            tunel_image = pygame.image.load("imagenes/tunel.png")
            tunel_image = pygame.transform.scale(tunel_image, (GRID_SIZE_X, GRID_SIZE_Y))
        except:
            tunel_image = None
        
        velocidad = 3
        Puntuacion = 0
        tiempo_inicio = pygame.time.get_ticks()
        juego_pausado = False
        tiempo_pausa_inicio = 0
        tiempo_total_pausado = 0
        
        wall_group = pygame.sprite.Group()
        liana_group = pygame.sprite.Group()
        tunel_group = pygame.sprite.Group()
        zona_segura_group = pygame.sprite.Group()
        
        reloj = pygame.time.Clock()
        
        world_data = []
        with open('mapa_generado.txt', 'r') as world:
            for line in world:
                world_data.append(line.strip())
        
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
        
        # Encontrar spawn del jugador (centro)
        spawn_position = (GRID_COLS // 2, GRID_ROWS // 2)
        for row, tiles in enumerate(world_data):
            for col, tile in enumerate(tiles):
                if tile == '0' and abs(col - GRID_COLS // 2) < 3 and abs(row - GRID_ROWS // 2) < 3:
                    spawn_position = (col, row)
                    break
        
        spawn_x_pixel = spawn_position[0] * GRID_SIZE_X + (GRID_SIZE_X - int(GRID_SIZE_X * 0.8)) // 2
        spawn_y_pixel = spawn_position[1] * GRID_SIZE_Y + (GRID_SIZE_Y - int(GRID_SIZE_Y * 0.8)) // 2
        jugador = Personaje(spawn_x_pixel, spawn_y_pixel, colorJugador, clase="cazador",
                           GRID_SIZE_X=GRID_SIZE_X, GRID_SIZE_Y=GRID_SIZE_Y,
                           WINDOW_WIDTH=WINDOW_WIDTH, WINDOW_HEIGHT=WINDOW_HEIGHT)
        
        # Crear zona segura en una esquina aleatoria
        esquinas = [
            (1, 1),  # Superior izquierda
            (GRID_COLS - 4, 1),  # Superior derecha
            (1, GRID_ROWS - 4),  # Inferior izquierda
            (GRID_COLS - 4, GRID_ROWS - 4)  # Inferior derecha
        ]
        zona_pos = random.choice(esquinas)
        zona_segura = ZonaSegura(zona_pos[0], zona_pos[1], GRID_SIZE_X, GRID_SIZE_Y)
        zona_segura_group.add(zona_segura)
        
        # Crear presas (enemigos)
        presas = []
        for i in range(NUM_PRESAS):
            presa_spawn = None
            intentos = 0
            
            while not presa_spawn and intentos < 100:
                intentos += 1
                for row, tiles in enumerate(world_data):
                    for col, tile in enumerate(tiles):
                        if tile == '0':
                            dist_x = abs(col - spawn_position[0])
                            dist_y = abs(row - spawn_position[1])
                            
                            # Evitar spawn en zona segura
                            dist_zona_x = abs(col - zona_pos[0])
                            dist_zona_y = abs(row - zona_pos[1])
                            
                            muy_cerca_de_otros = False
                            for otra_presa in presas:
                                otro_grid_x = otra_presa.x // GRID_SIZE_X
                                otro_grid_y = otra_presa.y // GRID_SIZE_Y
                                dist_otro_x = abs(col - otro_grid_x)
                                dist_otro_y = abs(row - otro_grid_y)
                                if dist_otro_x + dist_otro_y < 5:
                                    muy_cerca_de_otros = True
                                    break
                            
                            if dist_x + dist_y > 8 and not muy_cerca_de_otros and (dist_zona_x > 5 or dist_zona_y > 5):
                                presa_spawn = (col, row)
                                break
                    if presa_spawn:
                        break
            
            if presa_spawn:
                presa_x_pixel = presa_spawn[0] * GRID_SIZE_X + (GRID_SIZE_X - int(GRID_SIZE_X * 0.8)) // 2
                presa_y_pixel = presa_spawn[1] * GRID_SIZE_Y + (GRID_SIZE_Y - int(GRID_SIZE_Y * 0.8)) // 2
                nueva_presa = Personaje(presa_x_pixel, presa_y_pixel, colorPresa, clase="presa", es_enemigo=True,
                                   GRID_SIZE_X=GRID_SIZE_X, GRID_SIZE_Y=GRID_SIZE_Y,
                                   WINDOW_WIDTH=WINDOW_WIDTH, WINDOW_HEIGHT=WINDOW_HEIGHT)
                nueva_presa.velocidad_enemigo = 3.5
                nueva_presa.buscando_zona = False
                nueva_presa.tiempo_ultima_busqueda = pygame.time.get_ticks()
                nueva_presa.tiempo_inicio_busqueda = 0
                nueva_presa.en_zona_segura = False
                presas.append(nueva_presa)
        
        def mover_presa(presa, jugador_obj, zona_obj):
            if not presa.vivo:
                return
            
            tiempo_actual = pygame.time.get_ticks()
            
            # Verificar si debe buscar zona segura
            if not presa.buscando_zona and tiempo_actual - presa.tiempo_ultima_busqueda >= INTERVALO_BUSQUEDA:
                presa.buscando_zona = True
                presa.tiempo_inicio_busqueda = tiempo_actual
                presa.tiempo_ultima_busqueda = tiempo_actual
            
            # Verificar si terminó el tiempo de búsqueda
            if presa.buscando_zona and tiempo_actual - presa.tiempo_inicio_busqueda >= DURACION_BUSQUEDA:
                presa.buscando_zona = False
            
            velocidad_actual = presa.velocidad_enemigo
            if presa.esta_en_liana(liana_group):
                velocidad_actual = max(1, velocidad_actual - 0.5)
            
            pos_anterior_x = presa.x
            pos_anterior_y = presa.y
            
            if presa.buscando_zona:
                # Ir hacia la zona segura
                dx = zona_obj.rect.centerx - presa.x
                dy = zona_obj.rect.centery - presa.y
                
                if abs(dx) > abs(dy):
                    if dx > 0:
                        presa.x += velocidad_actual
                    else:
                        presa.x -= velocidad_actual
                else:
                    if dy > 0:
                        presa.y += velocidad_actual
                    else:
                        presa.y -= velocidad_actual
            else:
                # Movimiento aleatorio normal
                if tiempo_actual - presa.tiempo_cambio_direccion >= presa.intervalo_cambio:
                    presa.direccion = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
                    presa.tiempo_cambio_direccion = tiempo_actual
                    presa.intervalo_cambio = random.randint(1000, 3000)
                
                if presa.direccion == 'LEFT':
                    presa.x -= velocidad_actual
                elif presa.direccion == 'RIGHT':
                    presa.x += velocidad_actual
                elif presa.direccion == 'UP':
                    presa.y -= velocidad_actual
                elif presa.direccion == 'DOWN':
                    presa.y += velocidad_actual
            
            if presa.colision_con_obstaculos(wall_group, tunel_group):
                presa.x = pos_anterior_x
                presa.y = pos_anterior_y
                if not presa.buscando_zona:
                    presa.direccion = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
            
            if presa.x < 0:
                presa.x = 0
            if presa.x + presa.image.get_width() >= WINDOW_WIDTH:
                presa.x = WINDOW_WIDTH - presa.image.get_width()
            if presa.y < 0:
                presa.y = 0
            if presa.y + presa.image.get_height() >= WINDOW_HEIGHT:
                presa.y = WINDOW_HEIGHT - presa.image.get_height()
        
        def movimiento_jugador():
            key = pygame.key.get_pressed()
            
            pos_anterior_x = jugador.x
            pos_anterior_y = jugador.y
            
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                jugador.x -= velocidad
                if jugador.x < 0:
                    jugador.x = 0
                elif jugador.colision_con_obstaculos(wall_group, tunel_group):
                    jugador.x = pos_anterior_x
            
            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                jugador.x += velocidad
                if jugador.x + jugador.image.get_width() >= WINDOW_WIDTH:
                    jugador.x = WINDOW_WIDTH - jugador.image.get_width()
                elif jugador.colision_con_obstaculos(wall_group, tunel_group):
                    jugador.x = pos_anterior_x
            
            if key[pygame.K_UP] or key[pygame.K_w]:
                jugador.y -= velocidad
                if jugador.y < 0:
                    jugador.y = 0
                elif jugador.colision_con_obstaculos(wall_group, tunel_group):
                    jugador.y = pos_anterior_y
            
            if key[pygame.K_DOWN] or key[pygame.K_s]:
                jugador.y += velocidad
                if jugador.y + jugador.image.get_height() >= WINDOW_HEIGHT:
                    jugador.y = WINDOW_HEIGHT - jugador.image.get_height()
                elif jugador.colision_con_obstaculos(wall_group, tunel_group):
                    jugador.y = pos_anterior_y
        
        ejecutando = True
        juego_terminado = False
        victoria = False
        volver_menu = False
        presas_capturadas = 0
        
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
            zona_segura_group.draw(ventana)
            
            if not juego_terminado and not juego_pausado:
                tiempo_actual = pygame.time.get_ticks()
                tiempo_transcurrido = tiempo_actual - tiempo_inicio - tiempo_total_pausado
                tiempo_restante = max(0, TIEMPO_LIMITE - tiempo_transcurrido)
                
                if tiempo_restante <= 0:
                    juego_terminado = True
                    # Guardar puntuación cuando el juego termina
                if juego_terminado and not hasattr(iniciar_modo_cazador, 'puntuacion_guardada'):
                    salonFama.guardar_puntuacion(jugador_nombre, Puntuacion, "cazador")
                    iniciar_modo_cazador.puntuacion_guardada = True
                    victoria = True
                    Puntuacion = Puntuacion * MULTIPLICADOR
                
                movimiento_jugador()
                
                # Mover presas
                for presa in presas:
                    mover_presa(presa, jugador, zona_segura)
                
                # Verificar captura de presas
                for presa in presas:
                    if jugador.colisiona_con(presa) and presa.vivo:
                        presa.vivo = False
                        presa.tiempo_muerte = tiempo_actual
                        presa.en_zona_segura = False
                        Puntuacion += 10
                        presas_capturadas += 1
                
                # Verificar presas en zona segura
                for presa in presas:
                    if presa.vivo and not presa.en_zona_segura:
                        if presa.rect.colliderect(zona_segura.rect):
                            presa.en_zona_segura = True
                            presa.vivo = False
                            presa.tiempo_muerte = tiempo_actual
                            if Puntuacion >= 10:
                                Puntuacion -= 10
                            else:
                                Puntuacion = 0
                
                # Revivir presas
                for presa in presas:
                    if not presa.vivo and (tiempo_actual - presa.tiempo_muerte >= 10000):
                        presa_spawn = None
                        for row, tiles in enumerate(world_data):
                            for col, tile in enumerate(tiles):
                                if tile == '0':
                                    dist_j = abs(col - spawn_position[0]) + abs(row - spawn_position[1])
                                    dist_z = abs(col - zona_pos[0]) + abs(row - zona_pos[1])
                                    if dist_j > 8 and dist_z > 5:
                                        presa_spawn = (col, row)
                                        break
                            if presa_spawn:
                                break
                        
                        if presa_spawn:
                            presa.x = presa_spawn[0] * GRID_SIZE_X + (GRID_SIZE_X - int(GRID_SIZE_X * 0.8)) // 2
                            presa.y = presa_spawn[1] * GRID_SIZE_Y + (GRID_SIZE_Y - int(GRID_SIZE_Y * 0.8)) // 2
                            presa.vivo = True
                            presa.en_zona_segura = False
                            presa.tiempo_ultima_busqueda = tiempo_actual
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return "menu"
                    elif evento.key == pygame.K_p and not juego_terminado:
                        juego_pausado = not juego_pausado
                        if juego_pausado:
                            tiempo_pausa_inicio = pygame.time.get_ticks()
                        else:
                            tiempo_total_pausado += pygame.time.get_ticks() - tiempo_pausa_inicio
                    elif evento.key == pygame.K_m and juego_terminado:
                        return "menu"
            
            # Panel superior
            panel_alto = 60
            panel = pygame.Surface((WINDOW_WIDTH, panel_alto))
            panel.set_alpha(180)
            panel.fill((0, 0, 0))
            ventana.blit(panel, (0, 0))
            
            texto_puntuacion = fuente_mediana.render(f"Puntuacion: {Puntuacion}", True, (255, 255, 255))
            ventana.blit(texto_puntuacion, (20, 15))
            
            if not juego_terminado:
                tiempo_actual = pygame.time.get_ticks()
                tiempo_transcurrido = tiempo_actual - tiempo_inicio - tiempo_total_pausado
                tiempo_restante = max(0, TIEMPO_LIMITE - tiempo_transcurrido)
                segundos_restantes = tiempo_restante // 1000
                minutos = segundos_restantes // 60
                segundos = segundos_restantes % 60
                
                color_tiempo = (255, 255, 255)
                if tiempo_restante < 30000:
                    color_tiempo = (255, 0, 0)
                elif tiempo_restante < 60000:
                    color_tiempo = (255, 255, 0)
                
                texto_tiempo = fuente_mediana.render(f"Tiempo: {minutos:02d}:{segundos:02d}", True, color_tiempo)
                ventana.blit(texto_tiempo, (WINDOW_WIDTH - 220, 15))
            
            texto_capturadas = fuente_pequena.render(f"Capturadas: {presas_capturadas}", True, (255, 255, 255))
            ventana.blit(texto_capturadas, (20, 70))
            
            jugador.update(ventana)
            for presa in presas:
                presa.update(ventana)
            
            if juego_terminado:
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                ventana.blit(overlay, (0, 0))
                
                if victoria:
                    texto_resultado = fuente_grande.render("¡VICTORIA!", True, (0, 255, 0))
                    texto_mensaje = fuente_mediana.render("¡Tiempo completado!", True, (255, 255, 255))
                
                texto_puntuacion = fuente_mediana.render(f"Puntuacion Final: {Puntuacion}", True, (255, 255, 255))
                texto_menu = fuente_mediana.render("Presiona M para volver al menu", True, (255, 255, 255))
                
                rect_resultado = texto_resultado.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
                rect_mensaje = texto_mensaje.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
                rect_puntuacion = texto_puntuacion.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
                rect_menu = texto_menu.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
                
                ventana.blit(texto_resultado, rect_resultado)
                ventana.blit(texto_mensaje, rect_mensaje)
                ventana.blit(texto_puntuacion, rect_puntuacion)
                ventana.blit(texto_menu, rect_menu)
            
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
    
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    iniciar_modo_cazador("Jugador")