SOURCES = tasks actors scale
NOTEBOOKDIR := RayAndAnyscaleBasics

CODE       = $(foreach sname, $(SOURCES), $(NOTEBOOKDIR)/$(sname).py)

all:
	jupytext --from=py:light --to ipynb $(CODE)

