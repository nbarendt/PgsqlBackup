#!/bin/bash

find tests -name "*.py" | xargs pep8
find tests -name "*.py" | xargs pyflakes

find bbpgsql -name "*.py" | xargs pep8
find bbpgsql -name "*.py" | xargs pyflakes

nosetests
