#!bash

isort setup.py
black setup.py

isort scrun
black scrun

isort example
black example

isort scrunner --skip __init__.py
black scrunner
