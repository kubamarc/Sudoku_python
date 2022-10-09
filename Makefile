.PHONY: all clean-temporary clean

all: sudoku.pdf backtrack.pdf okienko.pdf generowanie.pdf rozwiazywanie.pdf

sudoku.pdf: sudoku.md
	pandoc --metadata=title:"Dokumentacja sudoku.py" \
	 --from=markdown+abbreviations+tex_math_single_backslash \
	 --pdf-engine=pdflatex \
	 --variable=mainfont:"DejaVu Sans" \
	 --toc --toc-depth=4 \
	 --output=sudoku.pdf sudoku.md

sudoku.md: src/sudoku.py
	pdoc --pdf --force src/sudoku.py > sudoku.md

backtrack.pdf: backtrack.md
	pandoc --metadata=title:"Dokumentacja programu backtrack.py" \
	 --from=markdown+abbreviations+tex_math_single_backslash \
	 --pdf-engine=pdflatex \
	 --variable=mainfont:"DejaVu Sans" \
	 --toc --toc-depth=4 \
	 --output=backtrack.pdf backtrack.md

backtrack.md: src/backtrack.py
	pdoc --pdf --force src/backtrack.py > backtrack.md

okienko.pdf: okienko.md
	pandoc --metadata=title:"Dokumentacja programu okienko.py" \
	 --from=markdown+abbreviations+tex_math_single_backslash \
	 --pdf-engine=pdflatex \
	 --variable=mainfont:"DejaVu Sans" \
	 --toc --toc-depth=4 \
	 --output=okienko.pdf okienko.md

okienko.md: src/okienko.py
	pdoc --pdf --force src/okienko.py > okienko.md

generowanie.pdf: generowanie.md
	pandoc --metadata=title:"Dokumentacja programu generowanie.py" \
	 --from=markdown+abbreviations+tex_math_single_backslash \
	 --pdf-engine=pdflatex \
	 --variable=mainfont:"DejaVu Sans" \
	 --toc --toc-depth=4 \
	 --output=generowanie.pdf generowanie.md

generowanie.md: src/generowanie.py
	pdoc --pdf --force src/generowanie.py > generowanie.md

rozwiazywanie.pdf: rozwiazywanie.md
	pandoc --metadata=title:"Dokumentacja programu rozwiazywanie.py" \
	 --from=markdown+abbreviations+tex_math_single_backslash \
	 --pdf-engine=pdflatex \
	 --variable=mainfont:"DejaVu Sans" \
	 --toc --toc-depth=4 \
	 --output=rozwiazywanie.pdf rozwiazywanie.md

rozwiazywanie.md: src/rozwiazywanie.py
	pdoc --pdf --force src/rozwiazywanie.py > rozwiazywanie.md

clean-temporary:
	rm -f backtrack.md sudoku.md okienko.md generowanie.md rozwiazywanie.md

clean: clean-temporary
	rm -f backtrack.pdf sudoku.pdf okienko.pdf generowanie.pdf rozwiazywanie.pdf
