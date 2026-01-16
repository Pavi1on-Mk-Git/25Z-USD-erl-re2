#!/bin/bash
set -e

mkdir -p plots
pdm run scripts/draw_plot.py --env h1-walk-v0 --optimize theta --output-file plots/walk_theta.svg
pdm run scripts/draw_plot.py --env h1-walk-v0 --optimize frac --set-theta 0.8 --output-file plots/walk_frac.svg
pdm run scripts/draw_plot.py --env h1-walk-v0 --optimize time_steps --set-theta 0.8 --set-frac 0.2 --output-file plots/walk_time_steps.svg
pdm run scripts/draw_plot.py --env h1-walk-v0 --optimize K --set-theta 0.8 --set-frac 0.2 --set-time-steps 50 --output-file plots/walk_k.svg
