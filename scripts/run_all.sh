#!/bin/bash
set -e

PROC_COUNT=$(nproc)
HALF_PROC_COUNT=$(("$PROC_COUNT" / 2))

scripts/run.sh Ant-v2 0.5 0.7 200 1 "$PROC_COUNT"

pdm run scripts/compare_hyperparameter.py --env h1-walk-v0 --optimize theta --num-cpu "$HALF_PROC_COUNT" --max-processes 2
pdm run scripts/compare_hyperparameter.py --env h1-walk-v0 --optimize frac --num-cpu "$HALF_PROC_COUNT" --max-processes 2 \
    --set-theta 0.8
pdm run scripts/compare_hyperparameter.py --env h1-walk-v0 --optimize time_steps --num-cpu "$PROC_COUNT" --max-processes 1 \
    --set-theta 0.8 --set-frac 0.2
pdm run scripts/compare_hyperparameter.py --env h1-walk-v0 --optimize K --num-cpu "$PROC_COUNT" --max-processes 1 \
    --set-theta 0.8 --set-frac 0.2 --set-time-steps 50
pdm run scripts/compare_hyperparameter.py --env h1-walk-v0 --optimize seed --num-cpu "$HALF_PROC_COUNT" --max-processes 2 \
    --set-theta 0.8 --set-frac 0.2 --set-time-steps 50 --set-k 1

pdm run scripts/compare_hyperparameter.py --env h1-hurdle-v0 --optimize theta --num-cpu "$HALF_PROC_COUNT" --max-processes 2
pdm run scripts/compare_hyperparameter.py --env h1-hurdle-v0 --optimize frac --num-cpu "$HALF_PROC_COUNT" --max-processes 2 \
    --set-theta 0.7
pdm run scripts/compare_hyperparameter.py --env h1-hurdle-v0 --optimize time_steps --num-cpu "$PROC_COUNT" --max-processes 1 \
    --set-theta 0.7 --set-frac 0.2
pdm run scripts/compare_hyperparameter.py --env h1-hurdle-v0 --optimize K --num-cpu "$PROC_COUNT" --max-processes 1 \
    --set-theta 0.7 --set-frac 0.2 --set-time-steps 50
pdm run scripts/compare_hyperparameter.py --env h1-hurdle-v0 --optimize seed --num-cpu "$HALF_PROC_COUNT" --max-processes 2 \
    --set-theta 0.7 --set-frac 0.2 --set-time-steps 50 --set-k 1
