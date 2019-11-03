#!/usr/bin/env bash
export PYTHONPATH="${PWD}/../third"
echo $PYTHONPATH
uvicorn main:app --host=0.0.0.0 --port=8001
