#!/bin/bash

if hash python3 2>/dev/null; then
	python3 -B menu.py
elif hash python 2>/dev/null; then
	python -B menu.py
else
	echo "Could not find an installed version of Python in any of the following: $PATH"
fi
