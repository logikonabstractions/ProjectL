#!/bin/sh

python3 -u -m unittest discover -s tests -p 'test_*.py'
#python3 -u -m unittest discover -p 'test_*.py'