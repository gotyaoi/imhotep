#!/bin/bash

if hash python 2>/dev/null; then
	python menu.py
else
	echo "Could not find an installed Python 3.4 or later in any of the following: $PATH"
fi