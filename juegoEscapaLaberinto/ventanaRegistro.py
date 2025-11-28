import pygame
import sys

# Variable global para almacenar el nombre del jugador
nombre_jugador = ""

def ventana_registro():
    """
    Muestra la ventana de registro para ingresar el nombre del jugador.
    Retorna: True si se ingresó un nombre, False si se cerró la ventana
    """
    global nombre_jugador
    
    # Inicializar Pygame si no está inicializado
    if not pygame.get_init():
        pygame.init()
    
    # Configuración de la ventana
    ANCHO = 650
    ALTO = 450
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Escapa del Laberinto - Registro")
    
    # Cargar y escalar la imagen de fondo (opcional)
    try:
        fondo = pygame.image.load("imagenes/fondoMenu.png")
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    except pygame.error:
        # Crear un fondo alternativo si no se encuentra la imagen
        fondo = pygame.Surface((ANCHO, ALTO))
        fondo.fill((135, 206, 235))  # Color celeste
    
    # Configurar fuentes
    fuente_titulo = pygame.font.Font(None, 60)
    fuente_texto = pygame.font.Font(None, 40)
    fuente_input = pygame.font.Font(None, 48)
    
    # Variables para el input de texto
    texto_input = ""
    input_activo = True
    color_input_activo = (100, 100, 100)
    color_input_inactivo = (60, 60, 60)
    color_input = color_input_activo
    
    # Rectángulo del campo de texto
    ancho_input = 400
    alto_input = 60
    x_input = (ANCHO - ancho_input) // 2
    y_input = 200
    rect_input = pygame.Rect(x_input, y_input, ancho_input, alto_input)
    
    # Clase para el botón de continuar
    class Boton:
        def __init__(self, texto, x, y, ancho, alto):
            self.texto = texto
            self.rect = pygame.Rect(x, y, ancho, alto)
            self.color_normal = (60, 60, 60)
            self.color_hover = (80, 80, 80)
            self.color_deshabilitado = (40, 40, 40)
            self.color_actual = self.color_normal
            self.border_radius = 7
            self.opacidad = int(255 * 0.85)
            self.habilitado = False
            
        def dibujar(self, superficie):
            # Determinar el color según el estado
            if not self.habilitado:
                color_usar = self.color_deshabilitado
            else:
                color_usar = self.color_actual
            
            # Crear superficie semitransparente para el botón
            superficie_boton = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            
            # Dibujar el fondo del botón con opacidad
            color_con_alpha = (*color_usar, self.opacidad)
            pygame.draw.rect(superficie_boton, color_con_alpha, superficie_boton.get_rect(), border_radius=self.border_radius)
            
            # Dibujar el texto del botón
            color_texto = (255, 255, 255) if self.habilitado else (120, 120, 120)
            texto_render = fuente_input.render(self.texto, True, color_texto)
            texto_rect = texto_render.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
            superficie_boton.blit(texto_render, texto_rect)
            
            # Dibujar la superficie del botón en la ventana principal
            superficie.blit(superficie_boton, self.rect.topleft)
        
        def verificar_hover(self, pos_mouse):
            if self.habilitado and self.rect.collidepoint(pos_mouse):
                self.color_actual = self.color_hover
                return True
            else:
                self.color_actual = self.color_normal
                return False
        
        def verificar_click(self, pos_mouse):
            return self.habilitado and self.rect.collidepoint(pos_mouse)
    
    # Crear botón de continuar
    padding = 10
    ancho_boton = 250
    alto_boton = 60
    x_boton = (ANCHO - ancho_boton) // 2
    y_boton = 320
    boton_continuar = Boton("Continuar", x_boton, y_boton, ancho_boton, alto_boton)
    
    # Reloj para controlar los FPS
    reloj = pygame.time.Clock()
    
    # Cursor parpadeante
    cursor_visible = True
    tiempo_cursor = 0
    
    # Bucle principal
    ejecutando = True
    while ejecutando:
        pos_mouse = pygame.mouse.get_pos()
        tiempo_delta = reloj.tick(60)
        
        # Manejar el parpadeo del cursor
        tiempo_cursor += tiempo_delta
        if tiempo_cursor >= 500:  # Parpadea cada 500ms
            cursor_visible = not cursor_visible
            tiempo_cursor = 0
        
        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Detectar tecla ESC para salir
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                
                # Manejar entrada de texto
                if input_activo:
                    if evento.key == pygame.K_RETURN:
                        if len(texto_input.strip()) > 0:
                            nombre_jugador = texto_input.strip()
                            return True
                    elif evento.key == pygame.K_BACKSPACE:
                        texto_input = texto_input[:-1]
                    else:
                        # Limitar a 20 caracteres
                        if len(texto_input) < 20:
                            texto_input += evento.unicode
            
            # Detectar click en el campo de texto
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_input.collidepoint(pos_mouse):
                    input_activo = True
                    color_input = color_input_activo
                else:
                    input_activo = False
                    color_input = color_input_inactivo
                
                # Detectar click en el botón
                if boton_continuar.verificar_click(pos_mouse):
                    nombre_jugador = texto_input.strip()
                    return True
        
        # Actualizar estado del botón
        boton_continuar.habilitado = len(texto_input.strip()) > 0
        boton_continuar.verificar_hover(pos_mouse)
        
        # Dibujar el fondo
        ventana.blit(fondo, (0, 0))
        
        # Dibujar título
        texto_titulo = "Escapa del Laberinto"
        ancho_texto_titulo, alto_texto_titulo = fuente_titulo.size(texto_titulo)
        x_titulo = (ANCHO - ancho_texto_titulo) // 2
        y_titulo = 40
        
        # Fondo semitransparente del título
        superficie_fondo_titulo = pygame.Surface((ANCHO, alto_texto_titulo + 20))
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
        
        # Dibujar instrucción
        texto_instruccion = "Ingresa tu nombre:"
        texto_render_instruccion = fuente_texto.render(texto_instruccion, True, (255, 255, 255))
        texto_rect_instruccion = texto_render_instruccion.get_rect(center=(ANCHO // 2, y_input - 40))
        
        # Fondo para la instrucción
        superficie_fondo_inst = pygame.Surface((texto_rect_instruccion.width + 20, texto_rect_instruccion.height + 10))
        superficie_fondo_inst.set_alpha(int(255 * 0.7))
        superficie_fondo_inst.fill((40, 40, 40))
        ventana.blit(superficie_fondo_inst, (texto_rect_instruccion.x - 10, texto_rect_instruccion.y - 5))
        ventana.blit(texto_render_instruccion, texto_rect_instruccion)
        
        # Dibujar campo de texto
        superficie_input = pygame.Surface((rect_input.width, rect_input.height), pygame.SRCALPHA)
        color_con_alpha = (*color_input, int(255 * 0.85))
        pygame.draw.rect(superficie_input, color_con_alpha, superficie_input.get_rect(), border_radius=7)
        ventana.blit(superficie_input, rect_input.topleft)
        
        # Dibujar borde del campo de texto si está activo
        if input_activo:
            pygame.draw.rect(ventana, (255, 255, 255), rect_input, 2, border_radius=7)
        
        # Dibujar texto ingresado
        texto_mostrar = texto_input if texto_input else ""
        texto_render = fuente_input.render(texto_mostrar, True, (255, 255, 255))
        ventana.blit(texto_render, (rect_input.x + 10, rect_input.y + 12))
        
        # Dibujar cursor parpadeante
        if input_activo and cursor_visible and len(texto_input) < 20:
            cursor_x = rect_input.x + 10 + texto_render.get_width() + 2
            cursor_y = rect_input.y + 10
            pygame.draw.line(ventana, (255, 255, 255), (cursor_x, cursor_y), (cursor_x, cursor_y + 40), 2)
        
        # Dibujar el botón de continuar
        boton_continuar.dibujar(ventana)
        
        # Actualizar la pantalla
        pygame.display.flip()

    return False


def mostrar_ventana_registro():
    """
    Función principal que inicia todo el flujo del juego desde el registro.
    Esta es la función que se debe llamar desde fuera del módulo.
    """
    # Imports locales para evitar dependencias circulares
    from . import menu
    from . import presaMode
    from . import cazadorMode
    from . import salonFama
    
    pygame.init()
    
    # Iniciar música del menú
    try:
        menu.play('music.mp3')
    except Exception as e:
        print(f"No se pudo cargar la música: {e}")
    
    # Mostrar ventana de registro
    if ventana_registro():
        print(f"Jugador registrado: {nombre_jugador}")
        
        # Cerrar ventana de registro
        pygame.quit()
        
        # LOOP PRINCIPAL DEL MENÚ
        while True:
            # Reinicializar pygame para el menú
            pygame.init()
            
            # Mostrar menú del juego
            modo_seleccionado = menu.menu_seleccion_modo()
            
            if modo_seleccionado is None:
                break
            
            print(f"Modo seleccionado por {nombre_jugador}: {modo_seleccionado}")
            
            # Si selecciona Salón de la Fama
            if modo_seleccionado == "salon_fama":
                pygame.quit()
                try:
                    salonFama.mostrar_salon_fama()
                except Exception as e:
                    print(f"Error al cargar salon de la fama: {e}")
                # Reiniciar música después del salón de la fama
                pygame.init()
                try:
                    menu.unpause()
                except:
                    try:
                        menu.play('music.mp3')
                    except:
                        pass
                continue  # Volver al menú
            
            # Pausar música antes de iniciar el juego
            try:
                menu.pause()
            except:
                pass
            
            # Cerrar ventana del menú antes de iniciar el juego
            pygame.quit()
            
            # Ejecutar el juego correspondiente
            resultado = None
            try:
                if modo_seleccionado == "presa":
                    resultado = presaMode.iniciar_juego(nombre_jugador)
                elif modo_seleccionado == "cazador":
                    resultado = cazadorMode.iniciar_modo_cazador(nombre_jugador)
            except Exception as e:
                print(f"Error al iniciar el juego: {e}")
                import traceback
                traceback.print_exc()
            
            # Reinicializar pygame para volver al menú
            pygame.init()
            
            # Reanudar música al volver al menú
            try:
                menu.unpause()
            except:
                try:
                    menu.play('music.mp3')
                except:
                    pass
            
            # Si resultado no es "menu", salir completamente
            if resultado != "menu":
                break
    else:
        print("Registro cancelado")
    
    pygame.quit()
    sys.exit()

mostrar_ventana_registro()
if __name__ == "__main__":
    # Si se ejecuta directamente este archivo
    mostrar_ventana_registro()