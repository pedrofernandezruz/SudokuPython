import pygame
import math
import numpy as np

## Está bien perrón en https://www.sudoku-online.org/

# Tablero principal
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Colores predefinidos
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)

# Constantes de botones
LEFT_BUTTON = 0
RIGHT_BUTTON = 2

# Framerate
FPS = 60

# Textos
pygame.font.init()  # Inicializar fonts
FONT = pygame.font.SysFont('comicsans', 40)

INITIAL_BOARD = np.array([
    [0, 6, 0,   8, 4, 0,    2, 0, 7],
    [0, 0, 0,   0, 0, 3,    0, 0, 5],
    [0, 0, 1,   7, 5, 0,    8, 0, 0],

    [6, 0, 0,   3, 0, 8,    0, 7, 0],
    [0, 0, 0,   0, 0, 4,    3, 5, 0],
    [0, 0, 0,   6, 0, 0,    0, 0, 0],

    [0, 7, 0,   0, 0, 0,    5, 6, 0],
    [5, 2, 3,   9, 0, 7,    0, 0, 4],
    [0, 0, 6,   5, 3, 0,    0, 0, 0]
])


# Dibuja las líneas del tablero
def draw_board(w_divisions, h_divisions):
    for w_div, w_pos in enumerate(w_divisions):
        pygame.draw.line(WIN, color=BLACK,
                         start_pos=(w_pos, 0), end_pos=(w_pos, HEIGHT-1),
                         width=3 if (w_div % 3 == 0) else 1)
    for h_div, h_pos in enumerate(h_divisions):
        pygame.draw.line(WIN, color=BLACK,
                         start_pos=(0, h_pos), end_pos=(WIDTH-1, h_pos),
                         width=3 if h_div % 3 == 0 else 1)


# Dibuja los números (y los colorea según su origen)
def draw_text(w_divisions, h_divisions, board, initial_board):
    for i in range(9):  # Divisiones en altura
        for j in range(9):  # Divisiones en anchura
            if board[i][j]:  # Si es distinto de 0, se escribe
                # El texto se dibuja en negro si es del original y en rojo si es nuevo
                text = FONT.render(str(board[i][j]), True, BLACK if initial_board[i][j] else RED)
                text_rect = text.get_rect(
                    center=(
                        (w_divisions[j+1]+w_divisions[j])//2,
                        (h_divisions[i+1]+h_divisions[i])//2
                    )
                )
                WIN.blit(text, text_rect)


# Resalta las casillas de colorines
def highlight_squares(w_divisions, h_divisions, hl_sq, highlightAll):
    hl_sq_w = hl_sq[1]
    hl_sq_h = hl_sq[0]

    if highlightAll:  # Sólo si hay que resaltar todo
        # Resaltar fila
        cyan_row = pygame.Rect((0, h_divisions[hl_sq_h]), (WIDTH, HEIGHT // 9))
        pygame.draw.rect(WIN, CYAN, cyan_row, width=0)  # Dibujar el cuadrado con relleno
        # Resaltar columna
        cyan_clm = pygame.Rect((w_divisions[hl_sq_w], 0), (WIDTH // 9, HEIGHT))
        pygame.draw.rect(WIN, CYAN, cyan_clm, width=0)  # Dibujar el cuadrado con relleno
        # Resaltar cuadrado grande
        cyan_sq = pygame.Rect((w_divisions[3*(hl_sq_w//3)], h_divisions[3*(hl_sq_h//3)]), (WIDTH // 3, HEIGHT // 3))
        pygame.draw.rect(WIN, CYAN, cyan_sq, width=0)  # Dibujar el cuadrado con relleno
    # Resaltar cuadrado pequeño
    yellow_sq = pygame.Rect((w_divisions[hl_sq_w], h_divisions[hl_sq_h]), (WIDTH // 9, HEIGHT // 9))
    pygame.draw.rect(WIN, YELLOW, yellow_sq, width=0)  # Dibujar el cuadrado con relleno


# Dibuja todos los elementos en la pantalla
def draw_window(w_divisions, h_divisions, hl_sq, board, initial_board, highlightAll=True):
    # Representar fondo
    WIN.fill(WHITE)
    # Resaltar casilla pulsada (si hay alguna)
    if hl_sq:
        highlight_squares(w_divisions, h_divisions, hl_sq, highlightAll)
    # Dibujar patrón del tablero
    draw_board(w_divisions, h_divisions)
    # Dibujar texto escrito
    draw_text(w_divisions, h_divisions, board, initial_board)
    # Actualizar display
    pygame.display.update()


# Calcula la posición del cuadrado a resaltar
def calculate_square(mouse_pos):
    # RATIOS PARA LOS COEFICIENTES: 9 (recuadro básico) -> WIDTH (recuadro extendido!!)
    # Deescalar de la misma forma para obtener directamente el recuadro
    w_ratio = WIDTH/9
    h_ratio = HEIGHT/9
    return math.floor(mouse_pos[1] / h_ratio), math.floor(mouse_pos[0] / w_ratio)


# Emular un switch con un diccionario
def parse_keys(key):
    switch = {
        pygame.K_1: 1,
        pygame.K_2: 2,
        pygame.K_3: 3,
        pygame.K_4: 4,
        pygame.K_5: 5,
        pygame.K_6: 6,
        pygame.K_7: 7,
        pygame.K_8: 8,
        pygame.K_9: 9
    }
    return switch.get(key, 0)  # Se añade 0 como valor por defecto


# Devuelve los game events en caso de que se necesiten
def get_events():
    return pygame.event.get()


def SudokuPlay():
    clock = pygame.time.Clock()
    run = True

    board = np.array(INITIAL_BOARD, dtype=np.uint8)  # Crear tablero en base al tablero inicial
    w_divisions = np.linspace(0, WIDTH-1, num=10, dtype=int)
    h_divisions = np.linspace(0, HEIGHT-1, num=10, dtype=int)
    hl_sq = None

    while run:
        # Fijar framerate
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Cerrar ventana
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:  # Click en la pantalla de algún botón
                # BOTÓN IZQUIERDO -> Seleccionar cuadrado
                if pygame.mouse.get_pressed()[LEFT_BUTTON]:  # Comprobar si se ha pulsado el botón izquierdo
                    mouse_pos = pygame.mouse.get_pos()  # Obtener la posición del ratón
                    hl_sq = calculate_square(mouse_pos)
                # BOTÓN DERECHO -> Limpiar selección
                if pygame.mouse.get_pressed()[RIGHT_BUTTON]:
                    hl_sq = None

            if event.type == pygame.KEYDOWN and hl_sq:
                # Debe haber una casilla seleccionada para pulsar botones

                # Si se pulsa la tecla enter!!
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    if not INITIAL_BOARD[hl_sq]:
                        board[hl_sq] = 0
                else:  # Comprobamos si la tecla pulsada es 1-9
                    number = parse_keys(event.key)
                    if number:  # Si se ha pulsado un número
                        if not INITIAL_BOARD[hl_sq]:
                            board[hl_sq] = number


        # Actualizar los cambios en la pantalla
        draw_window(w_divisions, h_divisions, hl_sq, board, INITIAL_BOARD)

    # Cerrar el juego al acabar
    pygame.quit()


if __name__ == "__main__":
    SudokuPlay()
