import pygame
import sys
import os

# Variable global para almacenar el nombre del jugador
nombre_jugador = ""

# Obtener la ruta del directorio donde está este archivo
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))

def cargar_imagen(nombre_archivo):
    """Carga una imagen desde la carpeta imagenes del módulo"""
    ruta = os.path.join(RUTA_BASE, 'imagenes', nombre_archivo)
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encuentra el archivo: {ruta}")
    return ruta

def ventana_registro():
    """
    Muestra la ventana de registro para ingresar el nombre del jugador.
    Retorna: True si se ingresó un nombre, False si se cerró la ventana
    """
    global nombre_jugador
    
    if not pygame.get_init():
        pygame.init()
    
    ANCHO = 650
    ALTO = 450
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Escapa del Laberinto - Registro")
    
    try:
        ruta_fondo = cargar_imagen("fondoMenu.png")
        fondo = pygame.image.load(ruta_fondo)
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    except (pygame.error, FileNotFoundError) as e:
        print(f"Advertencia: {e}")
        fondo = pygame.Surface((ANCHO, ALTO))
        fondo.fill((135, 206, 235))
    
    fuente_titulo = pygame.font.Font(None, 60)
    fuente_texto = pygame.font.Font(None, 40)
    fuente_input = pygame.font.Font(None, 48)
    
    texto_input = ""
    input_activo = True
    color_input_activo = (100, 100, 100)
    color_input_inactivo = (60, 60, 60)
    color_input = color_input_activo
    
    ancho_input = 400
    alto_input = 60
    x_input = (ANCHO - ancho_input) // 2
    y_input = 200
    rect_input = pygame.Rect(x_input, y_input, ancho_input, alto_input)
    
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
            if not self.habilitado:
                color_usar = self.color_deshabilitado
            else:
                color_usar = self.color_actual
            
            superficie_boton = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            color_con_alpha = (*color_usar, self.opacidad)
            pygame.draw.rect(superficie_boton, color_con_alpha, superficie_boton.get_rect(), border_radius=self.border_radius)
            
            color_texto = (255, 255, 255) if self.habilitado else (120, 120, 120)
            texto_render = fuente_input.render(self.texto, True, color_texto)
            texto_rect = texto_render.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
            superficie_boton.blit(texto_render, texto_rect)
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
    
    padding = 10
    ancho_boton = 250
    alto_boton = 60
    x_boton = (ANCHO - ancho_boton) // 2
    y_boton = 320
    boton_continuar = Boton("Continuar", x_boton, y_boton, ancho_boton, alto_boton)
    
    reloj = pygame.time.Clock()
    cursor_visible = True
    tiempo_cursor = 0
    
    ejecutando = True
    while ejecutando:
        pos_mouse = pygame.mouse.get_pos()
        tiempo_delta = reloj.tick(60)
        
        tiempo_cursor += tiempo_delta
        if tiempo_cursor >= 500:
            cursor_visible = not cursor_visible
            tiempo_cursor = 0
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                
                if input_activo:
                    if evento.key == pygame.K_RETURN:
                        if len(texto_input.strip()) > 0:
                            nombre_jugador = texto_input.strip()
                            return True
                    elif evento.key == pygame.K_BACKSPACE:
                        texto_input = texto_input[:-1]
                    else:
                        if len(texto_input) < 20:
                            texto_input += evento.unicode
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_input.collidepoint(pos_mouse):
                    input_activo = True
                    color_input = color_input_activo
                else:
                    input_activo = False
                    color_input = color_input_inactivo
                
                if boton_continuar.verificar_click(pos_mouse):
                    nombre_jugador = texto_input.strip()
                    return True
        
        boton_continuar.habilitado = len(texto_input.strip()) > 0
        boton_continuar.verificar_hover(pos_mouse)
        
        ventana.blit(fondo, (0, 0))
        
        texto_titulo = "Escapa del Laberinto"
        ancho_texto_titulo, alto_texto_titulo = fuente_titulo.size(texto_titulo)
        x_titulo = (ANCHO - ancho_texto_titulo) // 2
        y_titulo = 40
        
        superficie_fondo_titulo = pygame.Surface((ANCHO, alto_texto_titulo + 20))
        superficie_fondo_titulo.set_alpha(int(255 * 0.7))
        superficie_fondo_titulo.fill((40, 40, 40))
        ventana.blit(superficie_fondo_titulo, (0, y_titulo - 10))
        
        texto_borde = fuente_titulo.render(texto_titulo, True, (0, 0, 0))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ventana.blit(texto_borde, (x_titulo + dx * 0.45, y_titulo + dy * 0.45))
        
        texto_superficie = fuente_titulo.render(texto_titulo, True, (255, 255, 255))
        ventana.blit(texto_superficie, (x_titulo, y_titulo))
        
        texto_instruccion = "Ingresa tu nombre:"
        texto_render_instruccion = fuente_texto.render(texto_instruccion, True, (255, 255, 255))
        texto_rect_instruccion = texto_render_instruccion.get_rect(center=(ANCHO // 2, y_input - 40))
        
        superficie_fondo_inst = pygame.Surface((texto_rect_instruccion.width + 20, texto_rect_instruccion.height + 10))
        superficie_fondo_inst.set_alpha(int(255 * 0.7))
        superficie_fondo_inst.fill((40, 40, 40))
        ventana.blit(superficie_fondo_inst, (texto_rect_instruccion.x - 10, texto_rect_instruccion.y - 5))
        ventana.blit(texto_render_instruccion, texto_rect_instruccion)
        
        superficie_input = pygame.Surface((rect_input.width, rect_input.height), pygame.SRCALPHA)
        color_con_alpha = (*color_input, int(255 * 0.85))
        pygame.draw.rect(superficie_input, color_con_alpha, superficie_input.get_rect(), border_radius=7)
        ventana.blit(superficie_input, rect_input.topleft)
        
        if input_activo:
            pygame.draw.rect(ventana, (255, 255, 255), rect_input, 2, border_radius=7)
        
        texto_mostrar = texto_input if texto_input else ""
        texto_render = fuente_input.render(texto_mostrar, True, (255, 255, 255))
        ventana.blit(texto_render, (rect_input.x + 10, rect_input.y + 12))
        
        if input_activo and cursor_visible and len(texto_input) < 20:
            cursor_x = rect_input.x + 10 + texto_render.get_width() + 2
            cursor_y = rect_input.y + 10
            pygame.draw.line(ventana, (255, 255, 255), (cursor_x, cursor_y), (cursor_x, cursor_y + 40), 2)
        
        boton_continuar.dibujar(ventana)
        pygame.display.flip()
    
    return False


def mostrar_ventana_registro():
    """
    Función principal que inicia todo el flujo del juego desde el registro.
    """
    from . import menu
    from . import presaMode
    from . import cazadorMode
    from . import salonFama
    
    pygame.init()
    
    try:
        menu.play('music.mp3')
    except Exception as e:
        print(f"No se pudo cargar la música: {e}")
    
    if ventana_registro():
        print(f"Jugador registrado: {nombre_jugador}")
        pygame.quit()
        
        while True:
            pygame.init()
            modo_seleccionado = menu.menu_seleccion_modo()
            
            if modo_seleccionado is None:
                break
            
            print(f"Modo seleccionado por {nombre_jugador}: {modo_seleccionado}")
            
            if modo_seleccionado == "salon_fama":
                pygame.quit()
                try:
                    salonFama.mostrar_salon_fama()
                except Exception as e:
                    print(f"Error al cargar salon de la fama: {e}")
                pygame.init()
                try:
                    menu.unpause()
                except:
                    try:
                        menu.play('music.mp3')
                    except:
                        pass
                continue
            
            try:
                menu.pause()
            except:
                pass
            
            pygame.quit()
            
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
            
            pygame.init()
            
            try:
                menu.unpause()
            except:
                try:
                    menu.play('music.mp3')
                except:
                    pass
            
            if resultado != "menu":
                break
    else:
        print("Registro cancelado")
    
    pygame.quit()
    sys.exit()


# IMPORTANTE: Esta sección SOLO se ejecuta si ejecutas directamente este archivo
if __name__ == "__main__":
    mostrar_ventana_registro()