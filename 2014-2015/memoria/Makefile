# Makefile principal para generar la memoria

MEMORIA_LATEX = memoria

pdflatex:
	pdflatex $(MEMORIA_LATEX)
	-makeindex $(MEMORIA_LATEX)
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

	@echo Eliminando archivos de salida...
	@rm -f *.dvi

	@echo Orden clean terminada

distclean: clean
	@echo Eliminando pdf
	@rm -f *.pdf

	@echo Orden distclean terminada
