#!usr/bin/python3

import pygame

"""
Ustawienia kolorów i rozmiaru okna (nezmienialnego)
"""

rozmiar_okna = 700
kolor_tla = [None, None]
kolor_zablokowany = [None, None]
kolor_wstawiony = [None, None]
kolor_obramowania = [None, None]
kolor_kwadratu = [None, None]
kolor_tla[0] = (255, 255, 255)
kolor_tla[1] = (100, 100, 100)
kolor_zablokowany[0] = (100, 0, 0)
kolor_zablokowany[1] = (255, 100, 100)
kolor_wstawiony[0] = (0, 100, 0)
kolor_wstawiony[1] = (40, 210, 10)
kolor_obramowania[0] = (0, 0, 0)
kolor_obramowania[1] = (255, 255, 255)
kolor_kwadratu[0] = (255, 255, 0)
kolor_kwadratu[1] = kolor_kwadratu[0]
zielony = (0, 255, 0)
czerwony = (255, 0, 0)
niebieski = (100, 100, 220)


def pytanieOImie(okno):
    """
    Najpierw chcemy się dowiedzieć, kto będzie grać, żeby móc zapamiętać
    jego wynik i preferowaną (ostatnią) wersję kolorystyczną
    Imię może mieć maksymalnie 15 znaków
    """
    (x, y) = okno.get_size()
    font = pygame.font.SysFont('Corbel', (x + y) // 35)
    okno.fill(niebieski)
    podaj_imie = font.render('Podaj swoje imię', True, (0, 0, 0))
    okno.blit(podaj_imie, (x * 4 / 12, y * 1.2 / 12))
    imie = ''
    wpisany_znak = ''
    while not wpisany_znak == '\r':
        if len(imie) > 15:
            return imie
        pygame.display.flip()
        for e in [pygame.event.wait()] + pygame.event.get():
            if e.type == pygame.QUIT:
                return -1
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_BACKSPACE:
                    imie = imie[:-1]
                else:
                    wpisany_znak = e.unicode
                    if wpisany_znak != '\r':
                        imie += wpisany_znak
            i = font.render(imie, True, (0, 0, 0))
            okno.fill(niebieski)
            okno.blit(podaj_imie, (x * 4 / 12, y * 1.2 / 12))
            okno.blit(i, (70, 500))
    return imie


def narysujKwadrat(
        kwadrat_x,
        kwadrat_y,
        okno,
        kolor):
    """
    Chcemy oznaczać, w którym kwadraciku gry znajduje się gracz
    (co chce modyfikować), i w odpowiednim miejscu narysujemy żółty kwadracik,
    żeby wiedział gdzie jest.
    """

    kwadrat_x = min(8, kwadrat_x)
    kwadrat_y = min(8, kwadrat_y)
    (x, y) = okno.get_size()
    w1 = 8 + x * kwadrat_x / 9 - 1.5 * kwadrat_x
    w2 = 8 + y * kwadrat_y / 9 - 1.5 * kwadrat_y
    w3 = 4 + x * (kwadrat_x + 1) / 9 - 1.5 * kwadrat_x
    w4 = 4 + y * (kwadrat_y + 1) / 9 - 1.5 * kwadrat_y
    l_g = (w1, w2)
    l_d = (w1, w4)
    p_g = (w3, w2)
    p_d = (w3, w4)
    pygame.draw.polygon(okno, kolor_kwadratu[kolor], (l_g, p_g, p_d,
                        l_d))
    pygame.display.flip()


def wypiszLiczby(
        okno,
        sudoku,
        zablokowane,
        kolor):
    """
    Tutaj wypisujemy liczby, tak by gracz mógł zobaczyć je
    w odpowiednim kwadraciku gry
    """

    (x, y) = okno.get_size()
    x -= 20
    y -= 20
    font = pygame.font.SysFont('Corbel', (x + y) // 35)
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                pozycja_x = x / 17 + i * (x / 9)
                pozycja_y = y / 17 + j * (y / 9)
                if zablokowane[i][j]:
                    kolor_napisow = kolor_zablokowany[kolor]
                else:
                    kolor_napisow = kolor_wstawiony[kolor]
                wyp = font.render(str(sudoku[i][j]), zablokowane[i][j],
                                  kolor_napisow)
                okno.blit(wyp, (pozycja_x, pozycja_y))


def ustawieniaOkna(
        kolor,
        okno,
        sudoku,
        zablokowane,
        kwadrat_x,
        kwadrat_y,
        czy_sprzeczne,
        czy_rozwiazane):
    """
    Ta funkcja zajmuje się całościowym rysowaniem planszy, od wypełniania tła,
    poprzez rysowanie planszy, do wpisywania znaków do odpowiednich pól.
    Oczywiście niektóre zadania zleca podfunkcjom
    """

    if czy_sprzeczne:
        okno.fill(czerwony)
    elif czy_rozwiazane:
        okno.fill(zielony)
    else:
        okno.fill(kolor_tla[kolor])
    (x, y) = okno.get_size()
    x -= 20
    y -= 20

    narysujKwadrat(kwadrat_x, kwadrat_y, okno, kolor)

    for i in range(10):
        width_x = 5
        width_y = 5
        if i % 3 == 0:
            width_x = 10
            width_y = 10
        pygame.draw.line(
            okno,
            kolor_obramowania[kolor],
            (10 + x * i / 9, 20),
            (10 + x * i / 9, y),
            width_x,
        )
        pygame.draw.line(
            okno,
            kolor_obramowania[kolor],
            (20, 10 + y * i / 9),
            (x, 10 + y * i / 9),
            width_y,
        )
        # PEP8 takie linijki łyka, ale mnie się one średnio podobają :(
    wypiszLiczby(okno, sudoku, zablokowane, kolor)
    pygame.display.flip()


def instr(okno):
    """
    Funkcja programująca okno wyświetlające instrukcję do gry
    """
    (x, y) = okno.get_size()
    font = pygame.font.SysFont('Corbel', (x + y) // 35)
    okno.fill(niebieski)
    tekst = ["" for i in range(10)]
    tekst[0] = "Gra sudoku, trzeba wypełnić każdy wiersz,"
    tekst[1] = "kolumnę i 9 kwadratów wszystkimi liczbami"
    tekst[2] = "od 1 do 9."
    tekst[3] = "Aby cofnąć ruch, wciśnij \"c\", aby zobaczyć"
    tekst[4] = "podpowiedź, wciśnij \"p\"."
    tekst[5] = "Aby wejść do menu, wciśnij \"m\", zaś,"
    tekst[6] = "żeby zobaczyć to okno, wciśnij \"h\"."
    tekst[7] = "Żeby zobaczyć wynik, wciśnij \"w\"."
    tekst[8] = "Miłej gry."
    tekst[9] = "Aby opuścić to okno wciśnij dowolny klawisz."
    for i in range(10):
        napis = font.render(tekst[i], True, kolor_tla[0])
        okno.blit(napis, (x / 15, (10 + y + (1000 * i)) / 16))
    pygame.display.flip()
    while True:
        for e in [pygame.event.wait()] + pygame.event.get():
            if e.type == pygame.QUIT:
                return "koniec"
            if e.type == pygame.KEYUP or e.type == pygame.MOUSEBUTTONDOWN:
                return


def pokazWynik(okno, wynik):
    (x, y) = okno.get_size()
    font = pygame.font.SysFont('Corbel', (x + y) // 35)
    okno.fill(niebieski)
    tekst = ["", ""]
    tekst[0] = "Twój wynik: "
    tekst[1] = str(wynik)
    for i in range(2):
        napis = font.render(tekst[i], True, kolor_tla[0])
        okno.blit(napis, (x / 15, (10 + y + (1000 * i)) / 10))
    pygame.display.flip()
    while True:
        for e in [pygame.event.wait()] + pygame.event.get():
            if e.type == pygame.QUIT:
                return "koniec"
            if e.type == pygame.KEYUP or e.type == pygame.MOUSEBUTTONDOWN:
                return


def menu(okno, kolor):
    """
    Tutaj jest zaprogramowana graficzna i interaktywna strona menu gry,
    do którego wchodzi się porzez wciśnięcie 'm' w grze.
    """

    (x, y) = okno.get_size()
    font = pygame.font.SysFont('Corbel', (x + y) // 35)
    mysz = [0, 0]
    okno.fill(kolor_tla[kolor])
    while True:
        (x, y) = okno.get_size()
        for j in range(6):
            t = 1 + j * 2
            if y * t / 14 <= mysz[1] <= y * (t + 1) / 14\
                    and x / 4 <= mysz[0] <= x * 3 / 4:
                pygame.draw.rect(
                    okno,
                    kolor_kwadratu[kolor],
                    [y / 4, x * t / 14, y / 2, x / 14])
            else:
                pygame.draw.rect(
                    okno,
                    kolor_tla[1 - kolor],
                    [y / 4, x * t / 14, y / 2, x / 14])

        nowa_gra = font.render('nowa gra', True, kolor_tla[kolor])
        zmien_kolor = font.render('zmiana koloru', True,
                                  kolor_tla[kolor])
        rozwiazanie = font.render('zobacz rozwiązanie', True,
                                  kolor_tla[kolor])
        ins = font.render('instrukcja', True, kolor_tla[kolor])
        op_menu = font.render('wyjdź z menu', True,
                              kolor_tla[kolor])
        koniec = font.render('koniec gry', True, kolor_tla[kolor])

        okno.blit(nowa_gra, (x * 5 / 12, y * 1.2 / 14))
        okno.blit(zmien_kolor, (x * 4.5 / 12, y * 3.2 / 14))
        okno.blit(rozwiazanie, (x * 3.9 / 12, y * 5.2 / 14))
        okno.blit(ins, (x * 4.9 / 12, y * 7.2 / 14))
        okno.blit(op_menu, (x * 4.5 / 12, y * 9.2 / 14))
        okno.blit(koniec, (x * 5 / 12, y * 11.2 / 14))
        pygame.display.flip()

        for e in [pygame.event.wait()] + pygame.event.get():

            if e.type == pygame.QUIT:
                return 'koniec'
            if e.type == pygame.MOUSEMOTION:
                mysz = e.pos
            if e.type == pygame.MOUSEBUTTONDOWN:
                mysz = e.pos
                w = -1
                for i in range(6):
                    t = 1 + i * 2
                    if y * t / 14 <= mysz[1] <= y * (t + 1) / 14\
                            and x / 4 <= mysz[0] <= x * 3 / 4:
                        w = i

                if w == 0:
                    return 'nowa_gra'
                if w == 1:
                    return 'zmien_kolor'
                if w == 2:
                    return 'rozwiazanie'
                if w == 3:
                    ev = instr(okno)
                    if ev == "koniec":
                        return "koniec"
                    return
                if w == 4:
                    return 'op_menu'
                if w == 5:
                    return 'koniec'
