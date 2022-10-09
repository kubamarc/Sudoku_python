#!/usr/bin/python3

from backtrack import rozwiazanie_sudoku
from random import randint


def generowanie(trudnosc, wielkosc=9):
    """
    Fukcja generująca losową, jednoznaczną zagadkę sudoku.
    Najpierw generuje losowe sudoku, a potem usuwa do 45 pól, w sposób
    zachowujący jednoznaczność.
    """
    puste_sudoku = [[0 for i in range(wielkosc)] for j in range(wielkosc)]
    pelne_sudoku = rozwiazanie_sudoku(puste_sudoku, 0)
    l_pol_do_usuniecia = 15 * trudnosc
    i = 0
    nieusuwalne = {}
    while i < l_pol_do_usuniecia:
        x = randint(0, 8)
        y = randint(0, 8)
        if pelne_sudoku[x][y] != 0:
            poprz = pelne_sudoku[x][y]
            pelne_sudoku[x][y] = 0
            i += 1
            if rozwiazanie_sudoku(pelne_sudoku, 1) > 1:
                pelne_sudoku[x][y] = poprz
                nieusuwalne[(x, y)] = True
                if len(nieusuwalne) == wielkosc * wielkosc - i:
                    l_pol_do_usuniecia = i
    zablokowane = [[True for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            if pelne_sudoku[i][j] == 0:
                zablokowane[i][j] = False
    return (pelne_sudoku, zablokowane)
