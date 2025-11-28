import pygame
import sys

def menu_seleccion_modo():
    """
    Muestra el menú de selección de modo de juego.
    Retorna: 'presa' o 'cazador' según la selección del jugador, o None si cierra
    """
    # Inicializar Pygame si no está inicializado
    if not pygame.get_init():
        pygame.init()
    
    # Configuración de la ventana
    ANCHO = 650
    ALTO = 450
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Escapa del Laberinto - Selección de Modo")
    
    # Cargar y escalar la imagen de fondo
    try:
        fondo = pygame.image.load("imagenes/fondoMenu.png")
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
        # Crear un fondo alternativo si no se encuentra la imagen
        fondo = pygame.Surface((ANCHO, ALTO))
        fondo.fill((135, 206, 235))  # Color celeste
    
    # Configurar fuentes
    fuente_titulo = pygame.font.Font(None, 60)
    fuente_botones = pygame.font.Font(None, 48)
    
    # Clase para los botones
    class Boton:
        def __init__(self, texto, x, y, ancho, alto):
            self.texto = texto
            self.rect = pygame.Rect(x, y, ancho, alto)
            self.color_normal = (60, 60, 60)
            self.color_hover = (80, 80, 80)
            self.color_actual = self.color_normal
            self.border_radius = 7
            self.opacidad = int(255 * 0.85)  # 85% de opacidad
            
        def dibujar(self, superficie):
            # Crear superficie semitransparente para el botón
            superficie_boton = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            
            # Dibujar el fondo del botón con opacidad y border radius
            color_con_alpha = (*self.color_actual, self.opacidad)
            pygame.draw.rect(superficie_boton, color_con_alpha, superficie_boton.get_rect(), border_radius=self.border_radius)
            
            # Dibujar el texto del botón en la superficie
            texto_render = fuente_botones.render(self.texto, True, (255, 255, 255))
            texto_rect = texto_render.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
            superficie_boton.blit(texto_render, texto_rect)
            
            # Dibujar la superficie del botón en la ventana principal
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
    
    # Crear los botones con padding incluido en el tamaño
    padding = 10
    ancho_texto_boton = 230  # Ancho del área de texto
    alto_texto_boton = 40    # Alto del área de texto
    ancho_boton = ancho_texto_boton + (padding * 2)
    alto_boton = alto_texto_boton + (padding * 2)
    x_centrado = (ANCHO - ancho_boton) // 2
    y_primer_boton = 160
    
    boton_presa = Boton("Modo Presa", x_centrado, y_primer_boton, ancho_boton, alto_boton)
    boton_cazador = Boton("Modo Cazador", x_centrado, y_primer_boton + alto_boton + 20, ancho_boton, alto_boton)
    boton_salon = Boton("Ranking", x_centrado, y_primer_boton + (alto_boton + 20) * 2, ancho_boton, alto_boton)
    
    # Reloj para controlar los FPS
    reloj = pygame.time.Clock()
    
    # Variable para retornar la selección
    seleccion = None
    
    # Bucle principal del menú
    ejecutando = True
    while ejecutando:
        pos_mouse = pygame.mouse.get_pos()
        
        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Detectar tecla ESC para salir
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return None
            
            # Detectar clicks en los botones
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_presa.verificar_click(pos_mouse):
                    seleccion = "presa"
                    ejecutando = False
                elif boton_cazador.verificar_click(pos_mouse):
                    seleccion = "cazador"
                    ejecutando = False
                elif boton_salon.verificar_click(pos_mouse):
                    seleccion = "salon_fama"
                    ejecutando = False
        
        # Verificar hover en los botones
        boton_presa.verificar_hover(pos_mouse)
        boton_cazador.verificar_hover(pos_mouse)
        boton_salon.verificar_hover(pos_mouse)
        
        # Dibujar el fondo
        ventana.blit(fondo, (0, 0))
        
        # Dibujar el título "Selecciona el Modo" centrado en la parte superior
        texto_titulo = "Selecciona el Modo"
        ancho_texto, alto_texto = fuente_titulo.size(texto_titulo)
        x_titulo = (ANCHO - ancho_texto) // 2
        y_titulo = 40
        
        # Crear y dibujar fondo semitransparente detrás del título
        superficie_fondo_titulo = pygame.Surface((ANCHO, alto_texto + 20))
        superficie_fondo_titulo.set_alpha(int(255 * 0.7))  # 70% de opacidad
        superficie_fondo_titulo.fill((40, 40, 40))
        ventana.blit(superficie_fondo_titulo, (0, y_titulo - 10))
        
        # Dibujar borde más delgado (0.45px aproximadamente)
        texto_borde = fuente_titulo.render(texto_titulo, True, (0, 0, 0))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ventana.blit(texto_borde, (x_titulo + dx * 0.45, y_titulo + dy * 0.45))
        
        # Dibujar el texto principal
        texto_superficie = fuente_titulo.render(texto_titulo, True, (255, 255, 255))
        ventana.blit(texto_superficie, (x_titulo, y_titulo))
        
        # Dibujar los botones
        boton_presa.dibujar(ventana)
        boton_cazador.dibujar(ventana)
        boton_salon.dibujar(ventana)
        
        # Actualizar la pantalla
        pygame.display.flip()
        
        # Controlar los FPS (60 frames por segundo)
        reloj.tick(60)
    
    return seleccion


def menu_seleccion_dificultad():
    """
    Muestra el menú de selección de dificultad.
    Retorna: 'normal' o 'dificil' según la selección del jugador, o None si cierra
    """
    # Inicializar Pygame si no está inicializado
    if not pygame.get_init():
        pygame.init()
    
    # Configuración de la ventana
    ANCHO = 650
    ALTO = 450
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Escapa del Laberinto - Selección de Dificultad")
    
    # Cargar y escalar la imagen de fondo
    try:
        fondo = pygame.image.load("imagenes/fondoMenu.png")
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
        # Crear un fondo alternativo si no se encuentra la imagen
        fondo = pygame.Surface((ANCHO, ALTO))
        fondo.fill((135, 206, 235))  # Color celeste
    
    # Configurar fuentes
    fuente_titulo = pygame.font.Font(None, 60)
    fuente_botones = pygame.font.Font(None, 48)
    
    # Clase para los botones
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
    
    # Crear los botones
    padding = 10
    ancho_texto_boton = 230
    alto_texto_boton = 40
    ancho_boton = ancho_texto_boton + (padding * 2)
    alto_boton = alto_texto_boton + (padding * 2)
    x_centrado = (ANCHO - ancho_boton) // 2
    y_primer_boton = 180
    
    boton_normal = Boton("Normal", x_centrado, y_primer_boton, ancho_boton, alto_boton)
    boton_dificil = Boton("Difícil", x_centrado, y_primer_boton + alto_boton + 30, ancho_boton, alto_boton)
    
    # Reloj para controlar los FPS
    reloj = pygame.time.Clock()
    
    # Variable para retornar la selección
    seleccion = None
    
    # Bucle principal del menú
    ejecutando = True
    while ejecutando:
        pos_mouse = pygame.mouse.get_pos()
        
        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Detectar tecla ESC para volver atrás
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return None
            
            # Detectar clicks en los botones
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_normal.verificar_click(pos_mouse):
                    seleccion = "normal"
                    ejecutando = False
                elif boton_dificil.verificar_click(pos_mouse):
                    seleccion = "dificil"
                    ejecutando = False
        
        # Verificar hover en los botones
        boton_normal.verificar_hover(pos_mouse)
        boton_dificil.verificar_hover(pos_mouse)
        
        # Dibujar el fondo
        ventana.blit(fondo, (0, 0))
        
        # Dibujar el título
        texto_titulo = "Selecciona de Modo"
        ancho_texto, alto_texto = fuente_titulo.size(texto_titulo)
        x_titulo = (ANCHO - ancho_texto) // 2
        y_titulo = 40
        
        # Fondo semitransparente del título
        superficie_fondo_titulo = pygame.Surface((ANCHO, alto_texto + 20))
        superficie_fondo_titulo.set_alpha(int(255 * 0.7))
        superficie_fondo_titulo.fill((40, 40, 40))
        ventana.blit(superficie_fondo_titulo, (0, y_titulo - 10))
        
        # Dibujar borde del título
        texto_borde = fuente_titulo.render(texto_titulo, True, (0, 0, 0))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ventana.blit(texto_borde, (x_titulo + dx * 0.45, y_titulo + dy * 0.45))
        
        # Dibujar texto del título
        texto_superficie = fuente_titulo.render(texto_titulo, True, (255, 255, 255))
        ventana.blit(texto_superficie, (x_titulo, y_titulo))
        
        # Dibujar los botones
        boton_normal.dibujar(ventana)
        boton_dificil.dibujar(ventana)
        
        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(60)
    
    return seleccion


# Si se ejecuta directamente este archivo, mostrar el flujo completo de menús
if __name__ == "__main__":
    import presaMode
    import cazadorMode
    import salonFama
    
    pygame.init()
    
    while True:
        # Paso 1: Seleccionar modo
        modo_seleccionado = menu_seleccion_modo()
        
        if modo_seleccionado is None:
            break
        
        print(f"Modo seleccionado: {modo_seleccionado}")
        
        # Si selecciona Salón de la Fama
        if modo_seleccionado == "salon_fama":
            pygame.quit()
            salonFama.mostrar_salon_fama()
            pygame.init()
            continue
        
        # Cerrar ventana del menú antes de iniciar el juego
        pygame.quit()
        
        # Ejecutar el modo correspondiente
        if modo_seleccionado == "presa":
            presaMode.iniciar_juego()
        elif modo_seleccionado == "cazador":
            # El modo cazador tiene su propio menú de dificultad interno
            cazadorMode.iniciar_modo_cazador()
        
        # Reinicializar pygame para volver al menú
        pygame.init()
    
    pygame.quit()
    sys.exit()