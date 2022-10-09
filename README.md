# Gra Sudoku

## Uruchamianie

Uruchomić grę można poprzez uruchomienie skryptu `sudoku` znajdującego się
w tym katalogu.

```
./sudoku
```

## Dokumentacja

Aby wygenerować dokumentację został stworzony plik `Makefile` znajdujący się
w tym katalogu.

```
make
```

Aby usunąć wygenerowaną dokumentację, należy skorzystać z komendy:

```
make clean
```

A aby usunąć wyłącznie pliki pośrednie:

```
make clean-temporary
```


## Testy

W katalogu `tests/` jest test modułu 'backtrack' (w zasadzie ten z listy 11, na
podstawie którego budowany był projekt), który można uruchomić poleceniem
`python3 -m unittest` w tym katalogu.

## Zależności

* `pygame`
* `numpy`
