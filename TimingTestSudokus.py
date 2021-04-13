import SudokuSolveLogical as ssl
import SudokuSolve as ss
import SudokuTim as st
import time
import numpy as np

INITIAL_BOARD2 = np.array([
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

INITIAL_BOARD = np.array([
    [0, 0, 6, 7, 0, 3, 0, 0, 0],
    [0, 0, 0, 0, 9, 0, 7, 0, 4],
    [4, 0, 3, 0, 8, 0, 0, 0, 0],

    [9, 0, 5, 8, 0, 4, 1, 0, 7],
    [0, 2, 0, 6, 7, 0, 5, 9, 3],
    [0, 0, 0, 5, 0, 0, 0, 4, 0],

    [0, 8, 0, 3, 0, 0, 0, 0, 0],
    [0, 0, 7, 4, 0, 0, 6, 0, 0],
    [0, 0, 0, 0, 0, 7, 3, 5, 0]
])


def TimingTestSudokus(INITIAL_BOARD):
    showSteps = False  # Comparar sólo la resolución

    # Ejecución del primero
    start_time_1 = time.time()
    board1 = ss.SudokuSolve(INITIAL_BOARD, showSteps=showSteps)
    end_time_1 = time.time()

    # Ejecución del segundo
    start_time_2 = time.time()
    board2 = ssl.SudokuSolveLogical(INITIAL_BOARD, showSteps=showSteps)
    end_time_2 = time.time()

    # Ejecución del tercero
    board3 = INITIAL_BOARD.copy()
    start_time_3 = time.time()
    st.solve(board3)
    end_time_3 = time.time()

    # RESULTADOS
    if np.array_equal(board1, board2):
        print("Mismo resultado")
    else:
        print("Resultados distintos")
    print("Tiempo de ejecución del primero:", end_time_1-start_time_1)
    print("Tiempo de ejecución del segundo:", end_time_2-start_time_2)
    print("Tiempo de ejecución del tercero:", end_time_3 - start_time_3)


# Ejecutar sólo si se llama específicamente al programa
if __name__ == "__main__":
    TimingTestSudokus(INITIAL_BOARD)
