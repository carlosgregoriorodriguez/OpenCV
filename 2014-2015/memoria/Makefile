# Makefile principal para generar la memoria

MEMORIA_LATEX = memoria

pdflatex:
	pdflatex $(MEMORIA_LATEX)
# glossaries
	-makeglossaries $(MEMORIA_LATEX).tex
# Listar acrónimos
	-makeindex -t $(MEMORIA_LATEX).alg -s $(MEMORIA_LATEX).ist -o $(MEMORIA_LATEX).acr $(MEMORIA_LATEX).acn

# Listar glosario
	-makeindex -t $(MEMORIA_LATEX).glg -s $(MEMORIA_LATEX).ist -o $(MEMORIA_LATEX).gls $(MEMORIA_LATEX).glo
# glosstex
#       -glosstex $(MEMORIA_LATEX) $(GLOSARIO_LATEX)
#       -makeindex $(MEMORIA_LATEX).gxs -o $(MEMORIA_LATEX).glx -s glosstex.ist
	pdflatex $(MEMORIA_LATEX)
	pdflatex $(MEMORIA_LATEX)

clean:
	@echo Eliminando los archivos auxiliares
	@rm -f *.aux
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


	@echo Eliminando archivos de salida...
	@rm -f *.dvi

	@echo Orden clean terminada

distclean: clean
	@echo Eliminando pdf
	@rm -f *.pdf

	@echo Orden distclean terminada
