#!/usr/bin/python3

from generowanie import generowanie
import rozwiazywanie
from okienko import pytanieOImie, wypiszLiczby
from okienko import ustawieniaOkna, instr, pokazWynik, menu
from okienko import rozmiar_okna
import pygame
import json
from os.path import exists
from pathlib import Path


def policzZera(sudoku):
    """
    Funkcja licząca liczbę niewypełnionych pól w grze
    """

    liczba_zer = 0
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                liczba_zer += 1
    return liczba_zer


def main():
    """
    W main-ie ogarniamy całościową komunikację między różnymi kawałkami gry,
    oraz z graczem.
    Dane graczy zapisujemy do pliku .sudoku.
    Tutaj zlecamy stworzenie nowej zagadki, obsługujemy poruszanie się gracza
    po planszy (strzałki lub myszka), oraz jej wypełnianie.
    """

    path = str(Path(__file__).parent.absolute()) + "/.sudoku"
    print(path)
    if not exists(path):
        plik = open(path, 'w+')
    else:
        plik = open(path, 'r')
    jsn = plik.read()
    plik.close()
    czy_sprzeczne, czy_rozwiazane, czy_zob_rozwiazanie = (False, False, False)
    (sudoku, zablokowane) = generowanie(3)
    liczba_zer = policzZera(sudoku)
    kolor = 0
    pygame.init()
    rozmiar_okna_x = rozmiar_okna
    rozmiar_okna_y = rozmiar_okna
    okno = pygame.display.set_mode((rozmiar_okna_x, rozmiar_okna_y))
    pygame.display.set_caption('Sudoku (m by otworzyć menu)')
    pygame.display.update()
    if jsn == '':
        jsn = '{}'
    jsn = json.loads(jsn)
    imie = pytanieOImie(okno)
    if imie == -1:
        pygame.quit()
        return
    if imie in jsn:
        wynik = jsn[imie]['wynik']
        kolor = jsn[imie]['kolor']
    else:
        jsn[imie] = {'wynik': 0, 'kolor': 0}
        plik = open(path, 'w')
        plik.write(json.dumps(jsn))
        plik.close()
        res = instr(okno)
        if res == "koniec":
            pygame.quit()
            return
    kwadrat_x = 0
    kwadrat_y = 0
    ustawieniaOkna(
        kolor,
        okno,
        sudoku,
        zablokowane,
        kwadrat_x,
        kwadrat_y,
        czy_sprzeczne,
        czy_rozwiazane,
        )
    ruchy = []
    while True:
        for x in [pygame.event.wait()] + pygame.event.get():
            if x.type == pygame.QUIT:
                pygame.quit()
                return
            if x.type == pygame.KEYDOWN:
                if x.key == pygame.K_UP and kwadrat_y > 0:
                    kwadrat_y -= 1
                if x.key == pygame.K_DOWN and kwadrat_y < 8:
                    kwadrat_y += 1
                if x.key == pygame.K_LEFT and kwadrat_x > 0:
                    kwadrat_x -= 1
                if x.key == pygame.K_RIGHT and kwadrat_x < 8:
                    kwadrat_x += 1
                ustawieniaOkna(
                    kolor,
                    okno,
                    sudoku,
                    zablokowane,
                    kwadrat_x,
                    kwadrat_y,
                    czy_sprzeczne,
                    czy_rozwiazane,
                    )
            if x.type == pygame.KEYUP:
                if x.key == pygame.K_SPACE or x.key == pygame.K_BACKSPACE:
                    x.key = 48
                if x.key - 48 >= 0 and x.key - 48 < 10\
                        and not zablokowane[kwadrat_x][kwadrat_y]:
                    if sudoku[kwadrat_x][kwadrat_y] == 0 and x.key - 48 != 0:
                        liczba_zer -= 1
                    if sudoku[kwadrat_x][kwadrat_y] != 0 and x.key - 48 == 0:
                        liczba_zer += 1
                        czy_rozwiazane = False
                    if liczba_zer == 0 \
                            and rozwiazywanie.rozwiazanie(sudoku) is not None \
                            and not czy_zob_rozwiazanie:
                        czy_zob_rozwiazanie = True
                        czy_rozwiazane = True
                        jsn[imie]['wynik'] += 1
                        plik = open(path, 'w')
                        plik.write(json.dumps(jsn))
                        plik.close()
                    r = (kwadrat_x, kwadrat_y, sudoku[kwadrat_x][kwadrat_y])
                    ruchy.append(r)
                    sudoku[kwadrat_x][kwadrat_y] = x.key - 48
                    if czy_sprzeczne \
                            and rozwiazywanie.rozwiazanie(sudoku) is not None:
                        czy_sprzeczne = False
                    ustawieniaOkna(
                        kolor,
                        okno,
                        sudoku,
                        zablokowane,
                        kwadrat_x,
                        kwadrat_y,
                        czy_sprzeczne,
                        czy_rozwiazane,
                        )
                if x.unicode == 'h':
                    res = instr(okno)
                    if res == 'koniec':
                        pygame.quit()
                        return
                    ustawieniaOkna(
                        kolor,
                        okno,
                        sudoku,
                        zablokowane,
                        kwadrat_x,
                        kwadrat_y,
                        czy_sprzeczne,
                        czy_rozwiazane,
                        )
                if x.unicode == 'c':
                    czy_rozwiazane = False
                    if len(ruchy) > 0:
                        ru = ruchy[-1]
                        ruchy = ruchy[0:-1]
                        sudoku[ru[0]][ru[1]] = ru[2]
                        ustawieniaOkna(
                            kolor,
                            okno,
                            sudoku,
                            zablokowane,
                            kwadrat_x,
                            kwadrat_y,
                            czy_sprzeczne,
                            czy_rozwiazane,
                            )
                if x.unicode == 'p':
                    pod = rozwiazywanie.podpowiedz(sudoku)
                    czy_zob_rozwiazanie = True
                    if pod == "rozwiazana":
                        czy_rozwiazane = True
                    elif pod is None:
                        czy_sprzeczne = True
                    else:
                        sudoku[pod[0]][pod[1]] = pod[2]
                    ustawieniaOkna(
                        kolor,
                        okno,
                        sudoku,
                        zablokowane,
                        kwadrat_x,
                        kwadrat_y,
                        czy_sprzeczne,
                        czy_rozwiazane,
                        )
                if x.unicode == 'w':
                    res = pokazWynik(okno, jsn[imie]["wynik"])
                    if res == "koniec":
                        pygame.quit()
                        return
                    ustawieniaOkna(
                        kolor,
                        okno,
                        sudoku,
                        zablokowane,
                        kwadrat_x,
                        kwadrat_y,
                        czy_sprzeczne,
                        czy_rozwiazane,
                        )
                if x.unicode == 'm':
                    res = menu(okno, kolor)
                    if res == 'nowa_gra':
                        (czy_sprzeczne, czy_rozwiazane,
                         czy_zob_rozwiazanie) = (False, False, False)
                        (sudoku, zablokowane) = generowanie(3)
                    if res == 'zmien_kolor':
                        kolor = 1 - kolor
                        jsn[imie]['kolor'] = kolor
                        plik = open(path, 'w')
                        plik.write(json.dumps(jsn))
                        plik.close()
                    if res == 'rozwiazanie':
                        czy_zob_rozwiazanie = True
                        roz = rozwiazywanie.rozwiazanie(sudoku)
                        if roz is None:
                            czy_sprzeczne = True
                        else:
                            czy_rozwiazane = True
                            sudoku = roz
                            liczba_zer = 0
                    if res == 'op_menu':
                        pass
                    if res == 'koniec':
                        pygame.quit()
                        return
                    ustawieniaOkna(
                        kolor,
                        okno,
                        sudoku,
                        zablokowane,
                        kwadrat_x,
                        kwadrat_y,
                        czy_sprzeczne,
                        czy_rozwiazane,
                        )
            if x.type == pygame.MOUSEMOTION:
                (roz_x, roz_y) = okno.get_size()
                (pos_x, pos_y) = x.pos
                pos_x = 100 * pos_x / roz_x // 11
                pos_y = 100 * pos_y / roz_y // 11
                if kwadrat_x != int(pos_x) or kwadrat_y != int(pos_y):
                    kwadrat_x = int(pos_x)
                    kwadrat_y = int(pos_y)
                    ustawieniaOkna(
                        kolor,
                        okno,
                        sudoku,
                        zablokowane,
                        kwadrat_x,
                        kwadrat_y,
                        czy_sprzeczne,
                        czy_rozwiazane,
                        )


if __name__ == '__main__':
    main()
