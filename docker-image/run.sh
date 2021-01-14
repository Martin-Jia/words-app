#!/bin/bash
export FLASK_APP=/src/run.py
export PYTHONPATH="$PYTHONPATH:/src"
flask run --host=0.0.0.0 --port=80 2>&1 &
sleep infinity