#!/usr/bin/env bash

# defaults
PORT=8002

while getopts 'p:' flag; do
  case "${flag}" in
    p) PORT="${OPTARG}" ;;
  esac
done

main() {
  uvicorn src.app:app --host 0.0.0.0 --port "${PORT}" --reload --debug --workers 1 --log-level info
}

main
