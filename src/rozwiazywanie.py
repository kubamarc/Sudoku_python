#!/usr/bin/python3

from backtrack import rozwiazanie_sudoku
import copy
import random


def rozwiazanie(sudoku):
    """
    Funkcja pośrednicząca w automatycznym rozwiązaniu sudoku
    """
    return rozwiazanie_sudoku(sudoku, 0)


def podpowiedz(sudoku):
    """
    Funkcja losująca pole do podpowiedzi, i dająca jego wartość.
    """
    kopia = copy.deepcopy(sudoku)
    puste = []
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                puste.append((i, j))
                wyb = random.choice(puste)
    if len(puste) == 0:
        return "rozwiazana"
    kopia = rozwiazanie_sudoku(kopia, 0)
    if kopia is None:
        return None
    return (wyb[0], wyb[1], kopia[wyb[0]][wyb[1]])
