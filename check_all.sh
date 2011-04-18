#!/bin/bash
find bbpgsql tests -name "*.py" | xargs pyflakes
find bbpgsql/cmdline_scripts -name "*" | xargs pyflakes
pep8 bbpgsql/cmdline_scripts/archivewal
pep8 bbpgsql/cmdline_scripts/archivepgsql

