#!/bin/bash

if hash python3 2>/dev/null; then
	python3 menu.py
elif hash python 2>/dev/null; then
	if [[ `python -V` =~ "Python 3.4" || `python -V` =~ "Python 3.5" ]]; then
		python menu.py
	else
		echo "Python 3.4 or up is required."
	fi
else
	echo "Could not find an installed Python 3.4 or later in any of the following: $PATH"
fi