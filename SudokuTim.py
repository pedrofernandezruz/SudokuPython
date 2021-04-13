board = [
    [0, 6, 0, 8, 4, 0, 2, 0, 7],
    [0, 0, 0, 0, 0, 3, 0, 0, 5],
    [0, 0, 1, 7, 5, 0, 8, 0, 0],

    [6, 0, 0, 3, 0, 8, 0, 7, 0],
    [0, 0, 0, 0, 0, 4, 3, 5, 0],
    [0, 0, 0, 6, 0, 0, 0, 0, 0],

    [0, 7, 0, 0, 0, 0, 5, 6, 0],
    [5, 2, 3, 9, 0, 7, 0, 0, 4],
    [0, 0, 6, 5, 3, 0, 0, 0, 0]
]

board2 = [
    [0, 0, 6, 7, 0, 3, 0, 0, 0],
    [0, 0, 0, 0, 9, 0, 7, 0, 4],
    [4, 0, 3, 0, 8, 0, 0, 0, 0],

    [9, 0, 5, 8, 0, 4, 1, 0, 7],
    [0, 2, 0, 6, 7, 0, 5, 9, 3],
    [0, 0, 0, 5, 0, 0, 0, 4, 0],

    [0, 8, 0, 3, 0, 0, 0, 0, 0],
    [0, 0, 7, 4, 0, 0, 6, 0, 0],
    [0, 0, 0, 0, 0, 7, 3, 5, 0]
]


# Algoritmo como tal
def solve(board):

    # Comprobar si está el tablero resuelto o no
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    # Probar todos los valores
    for number in range(1, 10):
        # Si se puede colocar el número...
        if valid(board, number, (row, col)):
            # Se coloca el número
            board[row][col] = number
            # Se intentan colocar más números
            if solve(board):  # CORAZÓN DEL ALGORITMO -> RECURSIVIDAD
                return True
            # Si los números siguientes fallan, se vuelve hasta aquí y se borra
            board[row][col] = 0

    # Si ningún valor sirve, se indica hacia atrás
    return False


# Comprobar si un valor es válido en una posición
def valid(board, num, pos):
    rowPos = pos[0]
    colPos = pos[1]

    # Revisar que en la fila no esté repetido
    for j in range(len(board[0])):
        if board[rowPos][j] == num and colPos != j:
            return False

    # Revisar que en la columna no esté repetido
    for i in range(len(board)):
        if board[i][colPos] == num and rowPos != i:
            return False

    # Revisar en el recuadro que no esté repetido
    rowBox = rowPos // 3
    colBox = colPos // 3
    for i in range(rowBox*3, rowBox*3 + 3):
        for j in range(colBox*3, colBox*3 + 3):
            if board[i][j] == num and pos != (i, j):
                return False

    return True


# Muestra el tablero en texto
def print_board(board):
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:  # Dibujar un separador horizontal
            print("- - - - - - - - - - -")

        for j, num in enumerate(row):
            if j % 3 == 0 and j != 0:  # Dibujar un separador vertical
                print("| ", end="")  # Sin poner un \n

            print(str(num), end=" " if j != 8 else "\n")


# Encuentra casillas vacías
def find_empty(board):
    for i, row in enumerate(board):
        for j, num in enumerate(row):
            if num == 0:
                return i, j  # row, col

    return None  # No hay ninguna casilla vacía


if __name__ == "__main__":
    print_board(board2)
    solve(board2)
    print("", end="\n\n")
    print_board(board2)