#!/usr/bin/python3

import sys
import src.backtrack
import unittest
import types
import random
import math


class TestSudoku(unittest.TestCase):
    def poprawnyWiersz(self, s, i):
        liczby = [False for j in range(len(s))]
        for j in range(len(s)):
            liczby[s[i][j] - 1] = True
        for j in range(len(s)):
            if liczby[j] is False:
                return False
        return True


    def poprawnaKolumna(self, s, i):
        liczby = [False for j in range(len(s))]
        for j in range(len(s)):
            liczby[s[j][i] - 1] = True
        return (False not in liczby)


    def poprawnyKwadrat(self, s, i):
        liczby = [False for j in range(len(s))]
        x = (i % 3) * 3
        y = (i // 3) * 3
        for j in range(x, x + 3):
            for k in range(y, y + 3):
                liczby[s[j][k] - 1] = True
        return (False not in liczby)


    def poprawneSudoku(self, s):
        if s is None:
            return False
        for i in range(len(s)):
            if not self.poprawnaKolumna(s, i):
                return False
            if not self.poprawnyWiersz(s, i):
                return False
            if not self.poprawnyKwadrat(s, i):
                return False
        return True


    pusteSudoku = [[0 for i in range(9)] for j in range(9)]


    def testPusteSudoku(self):
        s = src.backtrack.rozwiazanie_sudoku(self.pusteSudoku, 0)
        self.assertEqual(self.poprawneSudoku(s), True)

    sprzeczneSudoku = [[0 for i in range(9)] for j in range(9)]
    sprzeczneSudoku[0][0] = 1
    sprzeczneSudoku[0][8] = 1

    def testSprzeczneSudoku(self):
        s = src.backtrack.rozwiazanie_sudoku(self.sprzeczneSudoku, 0)
        self.assertEqual(s, None)


    kolizjaWKolumnie = [[0 for i in range(9)] for j in range(9)]
    kolizjaWKolumnie[3][5] = 4
    kolizjaWKolumnie[7][5] = 4

    kolizjaWWierszu = [[0 for i in range(9)] for j in range(9)]
    kolizjaWWierszu[1][2] = 6
    kolizjaWWierszu[1][8] = 6

    kolizjaWKwadracie = [[0 for i in range(9)] for j in range(9)]
    kolizjaWKwadracie[0][5] = 4
    kolizjaWKwadracie[1][3] = 4

    def testColCollision(self):
        """
        Jest kolizja w kolumnie
        """
        res = src.backtrack.column_collision(5, self.kolizjaWKolumnie)
        self.assertEqual(res, True)
        """
        Brak kolizji w kolumnie
        """
        res = src.backtrack.column_collision(3, self.kolizjaWKolumnie)
        self.assertEqual(res, False)


    def testRowCollision(self):
        """
        Jest kolizja w wierszu
        """
        res = src.backtrack.row_collision(1, self.kolizjaWWierszu)
        self.assertEqual(res, True)
        """
        Brak kolizji w wierszu
        """
        res = src.backtrack.row_collision(2, self.kolizjaWWierszu)
        self.assertEqual(res, False)


    def testSquareCollision(self):
        """
        Jest kolizja w kwadracie
        """
        res = src.backtrack.square_collision(1, self.kolizjaWKwadracie)
        self.assertEqual(res, True)
        """
        Brak kolizji w kwadracie
        """
        res = src.backtrack.square_collision(5, self.kolizjaWKwadracie)
        self.assertEqual(res, False)


    def testNoCollision(self):
        """
        Kolizja w kwadracie
        """
        res = src.backtrack.no_collisions(self.kolizjaWKwadracie)
        self.assertEqual(res, False)
        """
        Kolizja w wierszu
        """
        res = src.backtrack.no_collisions(self.kolizjaWWierszu)
        self.assertEqual(res, False)
        """
        Kolizja w kolumnie
        """
        res = src.backtrack.no_collisions(self.kolizjaWKolumnie)
        self.assertEqual(res, False)
        """
        Brak kolizji
        """
        res = src.backtrack.no_collisions(self.pusteSudoku)
        self.assertEqual(res, True)



if __name__ == "__main__":
    unittest.main()
