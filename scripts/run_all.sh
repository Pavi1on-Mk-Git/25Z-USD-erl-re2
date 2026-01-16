#!/bin/bash
set -e

scripts/run.sh Ant-v2 0.5 0.7 200 1

pdm run scripts/compare_hyperparameter.py --env h1-walk-v0 --optimize theta --num-cpu 4 --max-processes 2
pdm run scripts/compare_hyperparameter.py --env h1-walk-v0 --optimize frac --num-cpu 4 --max-processes 2 \
    --set-theta 0.8
pdm run scripts/compare_hyperparameter.py --env h1-walk-v0 --optimize time_steps --num-cpu 8 --max-processes 1 \
    --set-theta 0.8 --set-frac 0.2
pdm run scripts/compare_hyperparameter.py --env h1-walk-v0 --optimize K --num-cpu 8 --max-processes 1 \
    --set-theta 0.8 --set-frac 0.2 --set-time-steps 50
pdm run scripts/compare_hyperparameter.py --env h1-walk-v0 --optimize seed --num-cpu 4 --max-processes 2 \
    --set-theta 0.8 --set-frac 0.2 --set-time-steps 50 --set-k 1

pdm run scripts/compare_hyperparameter.py --env h1-hurdle-v0 --optimize theta --num-cpu 4 --max-processes 2
pdm run scripts/compare_hyperparameter.py --env h1-hurdle-v0 --optimize frac --num-cpu 4 --max-processes 2 \
    --set-theta 0.7
pdm run scripts/compare_hyperparameter.py --env h1-hurdle-v0 --optimize time_steps --num-cpu 8 --max-processes 1 \
    --set-theta 0.7 --set-frac 0.2
pdm run scripts/compare_hyperparameter.py --env h1-hurdle-v0 --optimize K --num-cpu 8 --max-processes 1 \
    --set-theta 0.7 --set-frac 0.2 --set-time-steps 50
pdm run scripts/compare_hyperparameter.py --env h1-hurdle-v0 --optimize seed --num-cpu 4 --max-processes 2 \
    --set-theta 0.7 --set-frac 0.2 --set-time-steps 50 --set-k 1
