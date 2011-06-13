#!/bin/bash
find bbpgsql tests -name "*.py" | xargs pyflakes
find bbpgsql/cmdline_scripts -name "*" | xargs pyflakes
#find bbpgsql tests -name "*.py" -print -exec pyflakes \{\} \;
#find bbpgsql/cmdline_scripts -name "*" -print -exec pyflakes \{\} \;
pep8 bbpgsql/cmdline_scripts/archivewal
pep8 bbpgsql/cmdline_scripts/archivepgsql
pep8 bbpgsql
pep8 tests
