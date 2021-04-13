import numpy as np
import SudokuSolve as ss
from time import sleep

INITIAL_BOARD = np.array([
    [0, 6, 0, 8, 4, 0, 2, 0, 7],
    [0, 0, 0, 0, 0, 3, 0, 0, 5],
    [0, 0, 1, 7, 5, 0, 8, 0, 0],

    [6, 0, 0, 3, 0, 8, 0, 7, 0],
    [0, 0, 0, 0, 0, 4, 3, 5, 0],
    [0, 0, 0, 6, 0, 0, 0, 0, 0],

    [0, 7, 0, 0, 0, 0, 5, 6, 0],
    [5, 2, 3, 9, 0, 7, 0, 0, 4],
    [0, 0, 6, 5, 3, 0, 0, 0, 0]
])

# Definir un set de posibles valores
POSSIBLE_NUMBERS = {1, 2, 3, 4, 5, 6, 7, 8, 9}

def fill_tries_matrix(tries, INITIAL_BOARD):
    tries_new = ss.create_tries_matrix()

    for i in range(9):
        for j in range(9):
            if not INITIAL_BOARD[i][j]:
                tries_new[i][j] = ss.discard_values(list(POSSIBLE_NUMBERS), (i, j), INITIAL_BOARD, tries)

    return tries_new


# Avanza las posiciones
def next_sq(box_w, box_h):
    # Esquema extraño de avanzar por el cuadrado y por los números
    if box_w < 2:  # Si se puede avanzar en la fila...
        box_w += 1
    elif box_h < 2:  # Si se puede avanzar entre filas...
        box_w = 0
        box_h += 1
    else:
        box_w = 0
        box_h = 0


    return box_w, box_h


# Eliminar de la fila
def remove_from_row(tries, number, pos_h):
    for j in range(9):
        if number in tries[pos_h][j]:
            tries[pos_h][j].remove(number)


# Eliminar de la columna
def remove_from_col(tries, number, pos_w):
    for i in range(9):
        if number in tries[i][pos_w]:
            tries[i][pos_w].remove(number)


# Eliminar del bloque
def remove_from_sq(tries, number, pos):
    sq_w = pos[1]//3
    sq_h = pos[0]//3
    for i in range(3):
        for j in range(3):
            if number in tries[3*sq_h+i][3*sq_w+j]:
                tries[3 * sq_h + i][3 * sq_w + j].remove(number)


# Elimina los intentos de los lugares posibles
def remove_from_tries(tries, number, pos):
    pos_w = pos[1]
    pos_h = pos[0]

    # Eliminar de la fila
    remove_from_row(tries, number, pos_h)
    # Eliminar de la columna
    remove_from_col(tries, number, pos_w)
    # Eliminar del bloque
    remove_from_sq(tries, number, pos)


# Extrae un subarray
def get_subarray(tries, box_w, box_h):
    subarray = []
    for i in range(3):
        aux = []
        for j in range(3):
            aux.append(tries[3*box_h+i][3*box_w+j])
        subarray.append(aux)
    return subarray


# Devuelve el número de veces que aparece un número en un subarray
def numTimes(sub_tries, number):
    sum = 0
    for i in range(3):
        for j in range(3):
            sum += 1 if number in sub_tries[i][j] else 0
    return sum


# Encuentra la primera (y única) aparición de un valor en un subarray
def findPos(sub_tries, number):
    for i in range(3):
        for j in range(3):
            if number in sub_tries[i][j]:
                return i, j
    return None  # Por si acaso


# Encuentra si el número encaja en solitario en algún lugar de la casilla
def number_fits(tries, box_w, box_h, number):
    fits = False
    i = j = 0
    subarray = get_subarray(tries, box_w, box_h)

    # Se comprueba si en un recuadro el número está solo
    if numTimes(subarray, number) == 1:
        i, j = findPos(subarray, number)
        fits = True

    return fits, 3*box_h+i, 3*box_w+j


# Despeja columnas
def trim_cols(tries, box_w, box_h, number):
    isInCol = []
    # Buscar en columnas
    for j in range(3):
        isInCol.append(any(number in tries[3*box_h+i][3*box_w+j] for i in range(3)))

    # isInCol es ahora un vector de 3 posiciones con su presencia en las columnas
    # Hacemos una xor
    if sum(x for x in isInCol) == 1:
        # Se escoge la columna que va a trimmearse
        trimCol = 3*box_w + isInCol.index(True)
        for i in range(9):
            # Si no está en el bloque de interés y está entre las posibilidades, se quita del resto de bloques
            if i//3 != box_h and number in tries[i][trimCol]:
                tries[i][trimCol].remove(number)


# Despeja filas
def trim_rows(tries, box_w, box_h, number):
    isInRow = []
    # Buscar en columnas
    for i in range(3):
        isInRow.append(any(number in tries[3 * box_h + i][3 * box_w + j] for j in range(3)))

    # isInRow es ahora un vector de 3 posiciones con su presencia en las filas
    # Hacemos una xor
    if sum(x for x in isInRow) == 1:
        # Se escoge la columna que va a trimmearse
        trimRow = 3 * box_h + isInRow.index(True)
        for j in range(9):
            # Si no está en el bloque de interés y está entre las posibilidades, se quita del resto de bloques
            if j // 3 != box_w and number in tries[trimRow][j]:
                tries[trimRow][j].remove(number)


# Despeja de posibles soluciones
def trim_solutions(tries, box_w, box_h, number):
    # Despeja columnas
    trim_cols(tries, box_w, box_h, number)
    # Despeja filas
    trim_rows(tries, box_w, box_h, number)


# Devuelve los posibles valores que faltan por asignar en el recuadro
def remaining_values_in_sq(board, box_w, box_h):
    values = POSSIBLE_NUMBERS.copy()
    ss.discard_in_sq(values, (3*box_h, 3*box_w), board)
    return values


# Función principal
def SudokuSolveLogical(INITIAL_BOARD, showSteps=False):
    board = np.array(INITIAL_BOARD, dtype=np.uint8)  # Crear tablero en base al tablero inicial
    solving = True
    box_w = 0
    box_h = 0

    # Crear matriz con todos los intentos
    tries = fill_tries_matrix(ss.create_tries_matrix(), INITIAL_BOARD)

    while solving:
        for number in remaining_values_in_sq(board, box_w, box_h):

            # Trimear las posibles soluciones
            trim_solutions(tries, box_w, box_h, number)

            # Comprobar si el valor encaja en ese recuadro
            fits, i, j = number_fits(tries, box_w, box_h, number)
            if fits:
                # Añadir el valor a la tabla
                board[i][j] = number
                # Eliminar de la lista de posibilidades de fila, columna y bloque
                remove_from_tries(tries, number, (i, j))
                # Eliminar la lista de posibilidades de la casilla (ya ocupada)
                tries[i][j].clear()

            # Mostrar los pasos
            if showSteps:
                ss.update_board(board, INITIAL_BOARD, None, sleepMS=1)

        # Comprobar si se ha completado (todos los números > 0)
        if np.all(board > 0):
            solving = False
        else:
            box_w, box_h = next_sq(box_w, box_h)

    # Fin de ejecución, muestra la solución
    return board


# Ejecutar el programa
if __name__ == "__main__":
    showSteps = True

    # Mostrar tablero inicial
    ss.update_board(INITIAL_BOARD, INITIAL_BOARD, None)
    # Calcular tablero
    board = SudokuSolveLogical(INITIAL_BOARD, showSteps)
    # Mostrar resultados
    print(board)
    ss.update_board(board, INITIAL_BOARD, None)
    # Esperar
    sleep(5)
