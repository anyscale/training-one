install:
	jupytext --from=py:light src/tasks.py -o RayAndAnyscaleBasics/tasks.ipynb
	jupytext --from=py:light src/actors.py -o RayAndAnyscaleBasics/actors.ipynb
	jupytext --from=py:light src/scale.py -o RayAndAnyscaleBasics/scale.ipynb


