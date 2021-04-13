import numpy as np
import SudokuPlay as sp
from time import sleep

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

# Definir un set de posibles valores
POSSIBLE_NUMBERS = {1, 2, 3, 4, 5, 6, 7, 8, 9}


def discard_in_col(values, pos, board):
    fixed_w = pos[1]
    # Se recorren todas las filas
    for i in range(9):
        if board[i][fixed_w] in values:
            values.remove(board[i][fixed_w])

def discard_in_row(values, pos, board):
    fixed_h = pos[0]
    # Se recorren todas las filas
    for j in range(9):
        if board[fixed_h][j] in values:
            values.remove(board[fixed_h][j])

def discard_in_sq(values, pos, board):
    offset_h = pos[0] // 3
    offset_w = pos[1] // 3
    for i in range(3):
        for j in range(3):
            if board[3*offset_h+i][3*offset_w+j] in values:
                values.remove(board[3*offset_h+i][3*offset_w+j])


def discard_in_try(values, pos, tries):
    i = pos[0]
    j = pos[1]
    # Con List Comprehension ->
    # -> values = [val for val in values not in tries[i][j]]
    for val in tries[i][j]:  # Recorre todos los valores de los intentos
        if val in values:  # Comprueba si están en la lista
            values.remove(val)  # Los elimina


# Descarta los valores que no se podrían obtener
def discard_values(values, pos, board, tries):
    # Descarta los valores que ya estén en alguna columna
    discard_in_col(values, pos, board)
    # Descarta los valores que ya estén en una fila
    discard_in_row(values, pos, board)
    # Descarta los valores que ya estén en un recuadro
    discard_in_sq(values, pos, board)
    # Descarta los valores ya probados
    discard_in_try(values, pos, tries)
    # Devuelve la lista restante
    return values


# Desplaza hacia arriba o hacia abajo los números
def update_pos(i, j, up_or_down):
    if up_or_down:
        # Aumentar la cuenta
        if j < 8:
            j += 1
        else:
            j = 0
            i += 1
    else:
        # Decrementar la cuenta
        if j > 0:
            j -= 1
        else:
            j = 8
            i -= 1

    return i, j


# Crea una matriz de listas vacías
def create_tries_matrix():
    list = []  # Crea una lista vacía
    for i in range(9):  # Rellena todas las filas de listas vacías
        aux = []
        for j in range(9):  # Rellena una fila de listas vacías
            aux_2 = []
            aux.append(aux_2)

        list.append(aux)  # Añade la fila de listas vacías a la lista

    return list


# Ventana porque patata
def update_board(board, INITIAL_BOARD, pos, sleepMS=1):
    w_divisions = np.linspace(0, sp.WIDTH - 1, num=10, dtype=int)
    h_divisions = np.linspace(0, sp.HEIGHT - 1, num=10, dtype=int)
    sp.draw_window(w_divisions, h_divisions, pos, board, INITIAL_BOARD, False)
    # Ir a toda ostia sin sleep
    sleep(sleepMS/1000)  # Sleep 1 ms

    # Ignorar eventos
    for event in sp.get_events():
        pass


# Función principal
def SudokuSolve(INITIAL_BOARD, showSteps=False):
    board = np.array(INITIAL_BOARD, dtype=np.uint8)  # Crear tablero en base al tablero inicial
    solving = True
    i = 0
    j = 0

    uod = True

    tries = create_tries_matrix()

    while solving:
        # Solucionar fila a fila
        if not INITIAL_BOARD[i][j]:  # Solo se intenta si el tablero inicial no lo tiene
            poss_values = discard_values(list(POSSIBLE_NUMBERS), (i, j), board, tries)
            if len(poss_values):  # Si tiene algún elemento, se avanza
                board[i][j] = poss_values[0]  # Se le asigna el primer elemento
                tries[i][j].append(poss_values[0])  # Se guarda en la matriz de intentos
                uod = True  # Se fija incremento de posición

            else:  # Si se ha llegado a un punto muerto, hay que volver a atrás
                board[i][j] = 0
                tries[i][j].clear()  # Se borran los intentos de esta casilla (no son realmente válidos)
                uod = False  # Se fija decremento de posición

        # Actualizar posicion
        if i == 8 and j == 8 and uod:  # Si se ha alcanzado la posición final con éxito, se ha resuelto
            solving = False
        else:
            i, j = update_pos(i, j, up_or_down=uod)  # Actualizar posición

        if showSteps:
            update_board(board, INITIAL_BOARD, (i, j))

    # Fin de ejecución, muestra la solución
    return board


# Ejecutar el programa
if __name__ == "__main__":
    showSteps = False

    # Mostrar tablero inicial
    update_board(INITIAL_BOARD, INITIAL_BOARD, None)
    # Calcular tablero
    board = SudokuSolve(INITIAL_BOARD, showSteps)
    # Mostrar resultados
    print(board)
    update_board(board, INITIAL_BOARD, None)
    # Esperar
    sleep(5)
