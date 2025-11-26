import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO = 650
ALTO = 450
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Menú del Juego")

# Cargar y escalar la imagen de fondo
try:
    fondo = pygame.image.load("fondoMenu.png")
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
except pygame.error as e:
    print(f"No se pudo cargar la imagen: {e}")
    # Crear un fondo alternativo si no se encuentra la imagen
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill((135, 206, 235))  # Color celeste

# Configurar fuente para el título
fuente_titulo = pygame.font.Font(None, 60)

# Función para dibujar texto con borde
def dibujar_texto_con_borde(texto, fuente, color_texto, color_borde, x, y, grosor_borde):
    # Dibujar el borde (desplazando el texto en todas las direcciones)
    for dx in range(-grosor_borde, grosor_borde + 1):
        for dy in range(-grosor_borde, grosor_borde + 1):
            if dx != 0 or dy != 0:
                texto_borde = fuente.render(texto, True, color_borde)
                ventana.blit(texto_borde, (x + dx, y + dy))
    
    # Dibujar el texto principal encima
    texto_superficie = fuente.render(texto, True, color_texto)
    ventana.blit(texto_superficie, (x, y))

# Reloj para controlar los FPS
reloj = pygame.time.Clock()

# Bucle principal
ejecutando = True
while ejecutando:
    # Manejar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        
        # Detectar tecla ESC para salir
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False
    
    # Dibujar el fondo
    ventana.blit(fondo, (0, 0))
    
    # Dibujar el título "Menú de Dificultad" centrado en la parte superior
    texto_titulo = "Menú de Modos"
    ancho_texto, alto_texto = fuente_titulo.size(texto_titulo)
    x_titulo = (ANCHO - ancho_texto) // 2
    y_titulo = 40
    
    # Crear y dibujar fondo semitransparente detrás del título
    superficie_fondo_titulo = pygame.Surface((ANCHO, alto_texto + 25))
    superficie_fondo_titulo.set_alpha(int(255 * 0.7))  # 70% de opacidad
    superficie_fondo_titulo.fill((50, 50,50))
    ventana.blit(superficie_fondo_titulo, (0, y_titulo - 10))
    
    # Dibujar borde más delgado (0.45px aproximadamente)
    texto_borde = fuente_titulo.render(texto_titulo, True, (0, 0, 0))
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ventana.blit(texto_borde, (x_titulo + dx * 0.45, y_titulo + dy * 0.45))
    
    # Dibujar el texto principal
    texto_superficie = fuente_titulo.render(texto_titulo, True, (255, 255, 255))
    ventana.blit(texto_superficie, (x_titulo, y_titulo))
    
    # Actualizar la pantalla
    pygame.display.flip()
    
    # Controlar los FPS (60 frames por segundo)
    reloj.tick(60)

# Salir de Pygame
pygame.quit()
sys.exit()