#!/bin/bash
find bbpgsql tests -name "*.py" | xargs pyflakes
pep8 bbpgsql tests

