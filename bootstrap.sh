#!/bin/sh

# export PIPENV_VERBOSITY=-1
export FLASK_APP=./easyexps/index.py
pipenv run flask --debug run -h 0.0.0.0 -p 5050