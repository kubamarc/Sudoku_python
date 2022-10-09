#!/usr/bin/python3

import random
import numpy
import copy


def square_collision(i, sudoku):
    """
    Sprawdza, czy w kwadracie o numerze $i$ ma miejsce jakaś kolizja.
    Kolizją jest sytuacja, gdy występują przynajmniej dwie takie same liczby.
    """

    check = [0 for x in range(10)]
    start_x = i // 3
    start_x *= 3

    start_y = i - start_x
    start_y *= 3

    for j in range(0, 3):
        for k in range(0, 3):
            x = sudoku[start_x + j][start_y + k]
            check[x] += 1

    for j in range(1, 10):
        if check[j] > 1:
            return True

    return False


def row_collision(i, sudoku):
    """
    Sprawdza, czy w $i$-tym wierszu jest kolizja
    """

    check = [0 for x in range(10)]
    for j in range(0, 9):
        x = sudoku[i][j]
        check[x] += 1

    for j in range(1, 10):
        if check[j] > 1:
            return True

    return False


def column_collision(i, sudoku):
    """
    Sprawdza, czy w kolumnie $i$ zdarzyła sie kolizja.
    """

    check = [0 for x in range(10)]
    for j in range(0, 9):
        x = sudoku[j][i]
        check[x] += 1

    for j in range(1, 10):
        if check[j] > 1:
            return True

    return False


def any_collision(i, sudoku):
    """
    Sprawdza, czy w kolumnie $i$, wierszu $i$ lub kwadracie $i$ jest kolizja.
    Robi to, zlecając sprawdzenie odpowiednim podfunkcjom:
    row_collision, column_collision i square_collision.
    """

    return (square_collision(i, sudoku) or
            column_collision(i, sudoku) or row_collision(i, sudoku))


def no_collisions(sudoku):
    """
    Sprawdza, czy w całym sudoku nie ma kolizji.
    Robi to zlecając dla każdego i sprawdzenie funkcji any_collision
    """

    for i in range(0, 9):
        if any_collision(i, sudoku):
            return False
    return True


def backtrack(sudoku, i, j, tryb):
    """
    Backtrack rozwiązujący, lub zliczający rozwiązania sudoku.
    Działa rekurencyjnie, w każdym polu wsadzając liczby od 1 do 9
    (w losowej kolejności), a następnie, dla każdej z wsadzonych liczb
    uruchamiając się w następnym polu.
    W trybie 0 (rozwiązującym):
    Jeżeli kolejne wywołanie funkcji zwróci $False$, znaczy to, że dla
    obecnego wypełnienia sudoku nie ma rozwiązania, i trzeba spróbować inaczej
    Jeżeli zwróci sudoku (tablicę tablic), jest to rozwiązanie całego sudoku.
    Gdy następne wywołanie zwróci sudoku, od razu zwracamy je dalej.

    W trybie 1 (zliczającym):
    Jeżeli kolejne wywołanie funkcji zwróciło liczbę,
    trzeba ją dodać do wyniku.
    Jeżeli sudoku jest sprzeczne, zwracamy zero.
    Jeżeli doszliśmy do końca sudoku i mamy poprawne rozwiązanie, zwracamy 1.

    Za tryb pracy odpowiada zmienna $tryb$.
    """

    if tryb == 1:
        wynik = 0
    x = numpy.random.permutation(range(1, 10))
    if not no_collisions(sudoku):
        if tryb == 0:
            return False
        else:
            return 0
    if sudoku[i][j] == 0:
        for k in range(0, 9):
            sudoku[i][j] = x[k]
            if no_collisions(sudoku):
                if j == 8:
                    if i == 8:
                        if tryb == 0:
                            return sudoku
                        else:
                            return 1
                    else:
                        ret = backtrack(sudoku, i + 1, 0, tryb)
                        if ret is not False:
                            if tryb == 0:
                                return ret
                            else:
                                wynik += ret
                else:
                    ret = backtrack(sudoku, i, j + 1, tryb)
                    if ret is not False:
                        if tryb == 0:
                            return ret
                        else:
                            wynik += ret
        sudoku[i][j] = 0
        if tryb == 0:
            return False
        else:
            return wynik
    else:
        if j == 8:
            if i == 8:
                if tryb == 0:
                    return sudoku
                else:
                    return 1
            else:
                return backtrack(sudoku, i + 1, 0, tryb)
        else:
            return backtrack(sudoku, i, j + 1, tryb)


def rozwiazanie_sudoku(s, tryb):
    s = copy.deepcopy(s)
    res = backtrack(s, 0, 0, tryb)
    if res is False:
        return
    return res
