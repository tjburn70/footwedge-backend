#!/usr/bin/env bash

# defaults
PORT=8001

while getopts 'p:' flag; do
  case "${flag}" in
    p) PORT="${OPTARG}" ;;
  esac
done

main() {
  uvicorn src.main:app --host 0.0.0.0 --port "${PORT}" --reload --debug --workers 1 --log-level info
}

main
