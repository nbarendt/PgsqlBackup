#!/bin/bash
find . -name "*.pyc" | xargs rm
./run_tests.sh
./run_integration_tests.sh

