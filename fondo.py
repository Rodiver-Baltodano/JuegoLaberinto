import pygame
import sys

def iniciar_fondo():
    """Función que retorna el fondo escalado y las dimensiones del grid"""
    # Dimensiones de la ventana
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    
    # Calcular tamaño de celda para tener 38x24 cuadrados
    GRID_COLS = 38
    GRID_ROWS = 24
    GRID_SIZE_X = WINDOW_WIDTH // GRID_COLS
    GRID_SIZE_Y = WINDOW_HEIGHT // GRID_ROWS
    
    # Cargar la imagen de fondo
    try:
        background = pygame.image.load("Fondo.png")
        bg_width, bg_height = background.get_size()
        
        # Crear una superficie para el mapa completo (2x2 tiles)
        full_map = pygame.Surface((bg_width * 2, bg_height * 2))
        
        # Replicar la imagen 4 veces (2x2)
        full_map.blit(background, (0, 0))
        full_map.blit(background, (bg_width, 0))
        full_map.blit(background, (0, bg_height))
        full_map.blit(background, (bg_width, bg_height))
        
        # Escalar el mapa completo para que quepa en la ventana
        full_map_scaled = pygame.transform.scale(full_map, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        return full_map_scaled, WINDOW_WIDTH, WINDOW_HEIGHT, GRID_COLS, GRID_ROWS, GRID_SIZE_X, GRID_SIZE_Y
        
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
        print("Asegúrate de que 'Fondo.png' esté en el mismo directorio que este script.")
        # Crear un fondo negro como alternativa
        full_map_scaled = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        full_map_scaled.fill((0, 100, 0))  # Verde oscuro
        return full_map_scaled, WINDOW_WIDTH, WINDOW_HEIGHT, GRID_COLS, GRID_ROWS, GRID_SIZE_X, GRID_SIZE_Y

if __name__ == "__main__":
    # Si se ejecuta directamente, muestra el fondo con grid
    pygame.init()
    
    full_map_scaled, WINDOW_WIDTH, WINDOW_HEIGHT, GRID_COLS, GRID_ROWS, GRID_SIZE_X, GRID_SIZE_Y = iniciar_fondo()
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Mapa Grande con Fondo")
    
    clock = pygame.time.Clock()
    show_grid = True
    
    def draw_grid(surface, width, height, cols, rows):
        """Dibuja un grid sobre la superficie"""
        grid_color = (255, 255, 255, 100)
        
        cell_width = width / cols
        cell_height = height / rows
        
        # Líneas verticales
        for i in range(cols + 1):
            x = int(i * cell_width)
            pygame.draw.line(surface, grid_color, (x, 0), (x, height), 1)
        
        # Líneas horizontales
        for i in range(rows + 1):
            y = int(i * cell_height)
            pygame.draw.line(surface, grid_color, (0, y), (width, y), 1)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_g:
                    show_grid = not show_grid
        
        if full_map_scaled:
            screen.blit(full_map_scaled, (0, 0))
        
        if show_grid:
            draw_grid(screen, WINDOW_WIDTH, WINDOW_HEIGHT, GRID_COLS, GRID_ROWS)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()