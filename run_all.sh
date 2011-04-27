#!/bin/bash
find . -name "*.pyc" | xargs rm
./check_all.sh
nosetests tests
