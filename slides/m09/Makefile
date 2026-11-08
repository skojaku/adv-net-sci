# Build the slide-math decks in this directory.
#   make              v3 -> html + pdf
#   make check        check.py on v3 (0 errors expected)
#   make png          one PNG per slide + contact sheets (review/)
#   make all          html + pdf + png
#   make DECK=m08-gnn ...   build another deck
#   make clean        remove generated files
DECK  ?= m08-gnn-v3
SKILL ?= $(HOME)/.claude/skills/slide-math
RENDER = $(SKILL)/tools/render.sh
CHECK  = $(SKILL)/tools/check.py

.PHONY: default html pdf png all check clean

default: html pdf

html: $(DECK).html
pdf: $(DECK).pdf

$(DECK).html: $(DECK).md
	$(RENDER) $(DECK).md html

$(DECK).pdf: $(DECK).md
	$(RENDER) $(DECK).md pdf

# the sheets include every PNG in review/png, so PNGs of other decks show up in them
png:
	$(RENDER) $(DECK).md png

all: html pdf png

check:
	python3 $(CHECK) $(DECK).md

clean:
	rm -f $(DECK).html $(DECK).pdf review/png/$(DECK).*.png
