SOURCES = 01-tasks 02-actors 03-scale
NOTEBOOKDIR := RayAndAnyscaleBasics

CODE       = $(foreach sname, $(SOURCES), $(NOTEBOOKDIR)/$(sname).py)

all:
	jupytext --from=py:light --to ipynb $(CODE)

