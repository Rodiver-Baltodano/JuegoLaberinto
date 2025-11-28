import pygame
import sys
import json
import os

def cargar_puntuaciones():
    """Carga las puntuaciones desde el archivo JSON"""
    if os.path.exists('puntuaciones.json'):
        try:
            with open('puntuaciones.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def guardar_puntuacion(nombre_jugador, puntuacion, modo):
    """
    Guarda la puntuación de un jugador.
    Si el jugador ya existe, solo actualiza si la nueva puntuación es mayor.
    """
    puntuaciones = cargar_puntuaciones()
    
    # Crear clave única por jugador y modo
    clave = f"{nombre_jugador}_{modo}"
    
    # Si el jugador ya existe, solo actualizar si la nueva puntuación es mayor
    if clave in puntuaciones:
        if puntuacion > puntuaciones[clave]['puntuacion']:
            puntuaciones[clave] = {
                'nombre': nombre_jugador,
                'puntuacion': puntuacion,
                'modo': modo
            }
    else:
        puntuaciones[clave] = {
            'nombre': nombre_jugador,
            'puntuacion': puntuacion,
            'modo': modo
        }
    
    # Guardar en el archivo
    with open('puntuaciones.json', 'w', encoding='utf-8') as f:
        json.dump(puntuaciones, f, indent=4, ensure_ascii=False)

def obtener_top_10(modo=None):
    """
    Obtiene el top 10 de jugadores.
    Si se especifica un modo, filtra por ese modo.
    """
    puntuaciones = cargar_puntuaciones()
    
    # Convertir a lista
    lista_puntuaciones = []
    for clave, datos in puntuaciones.items():
        if modo is None or datos['modo'] == modo:
            lista_puntuaciones.append(datos)
    
    # Ordenar por puntuación descendente
    lista_puntuaciones.sort(key=lambda x: x['puntuacion'], reverse=True)
    
    # Retornar solo top 10
    return lista_puntuaciones[:10]

def mostrar_salon_fama():
    """Muestra la ventana del Salón de la Fama"""
    if not pygame.get_init():
        pygame.init()
    
    ANCHO = 800
    ALTO = 600
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Salón de la Fama")
    
    # Cargar fondo
    try:
        fondo = pygame.image.load("imagenes/fondoMenu.png")
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    except:
        fondo = pygame.Surface((ANCHO, ALTO))
        fondo.fill((135, 206, 235))
    
    # Fuentes
    fuente_titulo = pygame.font.Font(None, 70)
    fuente_tabs = pygame.font.Font(None, 40)
    fuente_tabla = pygame.font.Font(None, 32)
    fuente_pequeña = pygame.font.Font(None, 24)
    
    # Clase para los botones de pestañas
    class TabBoton:
        def __init__(self, texto, x, y, ancho, alto, activo=False):
            self.texto = texto
            self.rect = pygame.Rect(x, y, ancho, alto)
            self.activo = activo
            self.color_activo = (100, 100, 100)
            self.color_inactivo = (60, 60, 60)
            self.color_hover = (80, 80, 80)
            self.color_actual = self.color_activo if activo else self.color_inactivo
            self.border_radius = 7
            self.opacidad = int(255 * 0.85)
        
        def dibujar(self, superficie):
            superficie_boton = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            color_con_alpha = (*self.color_actual, self.opacidad)
            pygame.draw.rect(superficie_boton, color_con_alpha, superficie_boton.get_rect(), border_radius=self.border_radius)
            
            texto_render = fuente_tabs.render(self.texto, True, (255, 255, 255))
            texto_rect = texto_render.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
            superficie_boton.blit(texto_render, texto_rect)
            superficie.blit(superficie_boton, self.rect.topleft)
        
        def verificar_hover(self, pos_mouse):
            if self.rect.collidepoint(pos_mouse) and not self.activo:
                self.color_actual = self.color_hover
                return True
            else:
                self.color_actual = self.color_activo if self.activo else self.color_inactivo
                return False
        
        def verificar_click(self, pos_mouse):
            return self.rect.collidepoint(pos_mouse)
    
    # Crear botones de pestañas
    ancho_tab = 150
    alto_tab = 50
    y_tabs = 130
    
    tab_todos = TabBoton("Todos", 100, y_tabs, ancho_tab, alto_tab, activo=True)
    tab_presa = TabBoton("Presa", 270, y_tabs, ancho_tab, alto_tab)
    tab_cazador = TabBoton("Cazador", 440, y_tabs, ancho_tab, alto_tab)
    
    tabs = [tab_todos, tab_presa, tab_cazador]
    modo_actual = None  # None = todos, "presa" = presa, "cazador" = cazador
    
    reloj = pygame.time.Clock()
    ejecutando = True
    
    while ejecutando:
        pos_mouse = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if tab_todos.verificar_click(pos_mouse):
                    modo_actual = None
                    tab_todos.activo = True
                    tab_presa.activo = False
                    tab_cazador.activo = False
                elif tab_presa.verificar_click(pos_mouse):
                    modo_actual = "presa"
                    tab_todos.activo = False
                    tab_presa.activo = True
                    tab_cazador.activo = False
                elif tab_cazador.verificar_click(pos_mouse):
                    modo_actual = "cazador"
                    tab_todos.activo = False
                    tab_presa.activo = False
                    tab_cazador.activo = True
        
        # Verificar hover en tabs
        for tab in tabs:
            tab.verificar_hover(pos_mouse)
        
        # Dibujar fondo
        ventana.blit(fondo, (0, 0))
        
        # Dibujar título
        texto_titulo = "Salón de la Fama"
        ancho_texto, alto_texto = fuente_titulo.size(texto_titulo)
        x_titulo = (ANCHO - ancho_texto) // 2
        y_titulo = 30
        
        superficie_fondo_titulo = pygame.Surface((ANCHO, alto_texto + 20))
        superficie_fondo_titulo.set_alpha(int(255 * 0.7))
        superficie_fondo_titulo.fill((40, 40, 40))
        ventana.blit(superficie_fondo_titulo, (0, y_titulo - 10))
        
        texto_borde = fuente_titulo.render(texto_titulo, True, (0, 0, 0))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ventana.blit(texto_borde, (x_titulo + dx * 0.45, y_titulo + dy * 0.45))
        
        texto_superficie = fuente_titulo.render(texto_titulo, True, (255, 215, 0))
        ventana.blit(texto_superficie, (x_titulo, y_titulo))
        
        # Dibujar tabs
        for tab in tabs:
            tab.dibujar(ventana)
        
        # Obtener y mostrar puntuaciones
        top_10 = obtener_top_10(modo_actual)
        
        # Dibujar tabla de puntuaciones
        y_tabla = 210
        
        # Fondo de la tabla
        tabla_ancho = 700
        tabla_alto = 350
        tabla_x = (ANCHO - tabla_ancho) // 2
        superficie_tabla = pygame.Surface((tabla_ancho, tabla_alto))
        superficie_tabla.set_alpha(int(255 * 0.8))
        superficie_tabla.fill((30, 30, 30))
        ventana.blit(superficie_tabla, (tabla_x, y_tabla))
        
        # Encabezados
        texto_pos = fuente_tabla.render("Pos", True, (255, 215, 0))
        texto_nombre = fuente_tabla.render("Nombre", True, (255, 215, 0))
        texto_punt = fuente_tabla.render("Puntuación", True, (255, 215, 0))
        texto_modo = fuente_tabla.render("Modo", True, (255, 215, 0))
        
        ventana.blit(texto_pos, (tabla_x + 30, y_tabla + 15))
        ventana.blit(texto_nombre, (tabla_x + 120, y_tabla + 15))
        ventana.blit(texto_punt, (tabla_x + 350, y_tabla + 15))
        ventana.blit(texto_modo, (tabla_x + 550, y_tabla + 15))
        
        # Línea separadora
        pygame.draw.line(ventana, (255, 215, 0), 
                        (tabla_x + 20, y_tabla + 50), 
                        (tabla_x + tabla_ancho - 20, y_tabla + 50), 2)
        
        # Mostrar puntuaciones
        y_actual = y_tabla + 70
        for i, jugador in enumerate(top_10, 1):
            # Color según posición
            if i == 1:
                color = (255, 215, 0)  # Oro
            elif i == 2:
                color = (192, 192, 192)  # Plata
            elif i == 3:
                color = (205, 127, 50)  # Bronce
            else:
                color = (255, 255, 255)  # Blanco
            
            texto_pos = fuente_tabla.render(f"{i}", True, color)
            texto_nombre = fuente_tabla.render(jugador['nombre'][:15], True, color)
            texto_punt = fuente_tabla.render(str(jugador['puntuacion']), True, color)
            
            # Mostrar modo solo si estamos en "Todos"
            if modo_actual is None:
                modo_texto = "Presa" if jugador['modo'] == "presa" else "Cazador"
                texto_modo = fuente_tabla.render(modo_texto, True, color)
                ventana.blit(texto_modo, (tabla_x + 550, y_actual))
            
            ventana.blit(texto_pos, (tabla_x + 40, y_actual))
            ventana.blit(texto_nombre, (tabla_x + 120, y_actual))
            ventana.blit(texto_punt, (tabla_x + 370, y_actual))
            
            y_actual += 30
        
        # Si no hay puntuaciones
        if len(top_10) == 0:
            texto_vacio = fuente_tabla.render("No hay puntuaciones registradas", True, (150, 150, 150))
            rect_vacio = texto_vacio.get_rect(center=(ANCHO // 2, y_tabla + 150))
            ventana.blit(texto_vacio, rect_vacio)
        
        # Instrucción de salida
        texto_salir = fuente_pequeña.render("Presiona ESC para volver", True, (200, 200, 200))
        ventana.blit(texto_salir, (ANCHO // 2 - 120, ALTO - 40))
        
        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    pygame.init()
    mostrar_salon_fama()
    pygame.quit()
    sys.exit()