MAIN     = llm-uml-antipatterns
PDFLATEX = pdflatex
BIBTEX   = bibtex
FLAGS    = -interaction=nonstopmode -halt-on-error
PYTHON   = python3
CROP     = scripts/crop_title.py

# Matplotlib plots whose embedded titles should be stripped before inclusion.
# Add new plot filenames here as the paper grows.
PLOT_FIGS    = figures/finetune_loss_curve.png
CROPPED_FIGS = $(PLOT_FIGS:figures/%.png=figures/%_cropped.png)

figures/%_cropped.png: figures/%.png $(CROP)
	$(PYTHON) $(CROP) $< $@

.PHONY: all clean cleanall

all: $(CROPPED_FIGS) $(MAIN).pdf $(MAIN).md $(MAIN).docx

$(MAIN).pdf: $(MAIN).tex references.bib $(CROPPED_FIGS)
	$(PDFLATEX) $(FLAGS) $(MAIN)
	$(BIBTEX)   $(MAIN)
	$(PDFLATEX) $(FLAGS) $(MAIN)
	$(PDFLATEX) $(FLAGS) $(MAIN)

$(MAIN).md: $(MAIN).tex references.bib
	pandoc $(MAIN).tex --bibliography=references.bib --citeproc -o $(MAIN).md

$(MAIN).docx: $(MAIN).tex references.bib
	pandoc $(MAIN).tex --bibliography=references.bib --citeproc -o $(MAIN).docx

clean:
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).blg \
	      $(MAIN).log $(MAIN).out $(MAIN).toc \
	      $(MAIN).lof $(MAIN).lot $(MAIN).fls \
	      $(MAIN).fdb_latexmk $(MAIN).synctex.gz

cleanall: clean
	rm -f $(MAIN).pdf
