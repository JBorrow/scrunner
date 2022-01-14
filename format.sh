#!bash

isort setup.py
black setup.py

isort scrun
black scrun

isort example
black example

isort scrunner
black scrunner
