# Makefile principal para generar la memoria

MEMORIA_LATEX = memoria

# http://www.ctan.org/pkg/latexmk
latexmk:
# Realizar todo el proceso de compilación de la memoria con latexmk en
# vez de realizarlo manualmente y paso por paso porque latexmk siempre
# lo hará mejor, menos laborioso menos propenso a errores
# Añadir -shell-escape para que el paquete minted interactue con el
# paquete Pygments de Python

	latexmk -pdf \
	-synctex=1 \
	-r "glossaries.latexmk" \
	-pdflatex="pdflatex -interactive=nonstopmode  -shell-escape" \
	-use-make $(MEMORIA_LATEX).tex
#	pdflatex $(MEMORIA_LATEX)
# Generar bibliografía
	-bibtex $(MEMORIA_LATEX)
# glossaries
#	-makeglossaries $(MEMORIA_LATEX).tex
# Listar acrónimos
#	-makeindex -t $(MEMORIA_LATEX).alg -s $(MEMORIA_LATEX).ist -o $(MEMORIA_LATEX).acr $(MEMORIA_LATEX).acn

# Listar glosario
#	-makeindex -t $(MEMORIA_LATEX).glg -s $(MEMORIA_LATEX).ist -o $(MEMORIA_LATEX).gls $(MEMORIA_LATEX).glo
#	pdflatex $(MEMORIA_LATEX)
#	pdflatex $(MEMORIA_LATEX)
	@bash -c "xdg-open $(MEMORIA_LATEX).pdf" 2>/dev/null

clean:
	@echo Eliminando los archivos auxiliares
# Eliminamos de todas las carpetas de la memoria los *.aux
	@find . -name "*.aux" -type f -delete
	@rm -f *.out

	@echo Eliminando los archivos de registro
	@rm -f *.log

	@echo Eliminando los archivos que generan la lista de contenido
	@rm -f *.toc

	@echo Eliminando los archivos de generación del índices
	@rm -f *.ilg
	@rm -f *.ind
	@rm -f *.ist

	@echo Eliminando los archivos de generación del glosario
	@rm -f *.glg
	@rm -f *.gls
	@rm -f *.glo

	@echo Eliminando los archivos de generación de la lista de siglas
	@rm -f *.acn
	@rm -f *.acr
	@rm -f *.alg

	@echo Eliminando los archivos de generación de la bibliografía
	@rm -f *.bbl
	@rm -f *.blg


	@echo Eliminando archivos de salida...
	@rm -f *.dvi
	@rm -f *.fls
	@rm -f *.lof
	@rm -f *.pyg
	@rm -f *.fdb_latexmk
	@rm -f *.synctex.gz

	@echo Orden clean terminada

distclean: clean
	@echo Eliminando pdf
	@rm -f *.pdf

	@echo Orden distclean terminada
