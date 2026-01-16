#!/bin/bash
set -e

mkdir -p plots

pdm run scripts/draw_plot.py --env Ant-v2 --set-theta 0.5 --set-frac 0.7 --set-time-steps 200 --set-k 1 --set-seed 1 --output-file plots/ant.svg

pdm run scripts/draw_plot.py --env h1-walk-v0 --optimize theta --output-file plots/walk_theta.svg
pdm run scripts/draw_plot.py --env h1-walk-v0 --optimize frac --set-theta 0.8 --output-file plots/walk_frac.svg
pdm run scripts/draw_plot.py --env h1-walk-v0 --optimize time_steps --set-theta 0.8 --set-frac 0.2 --output-file plots/walk_time_steps.svg
pdm run scripts/draw_plot.py --env h1-walk-v0 --optimize K --set-theta 0.8 --set-frac 0.2 --set-time-steps 50 --output-file plots/walk_k.svg

pdm run scripts/draw_plot.py --env h1-hurdle-v0 --optimize theta --output-file plots/hurdle_theta.svg
pdm run scripts/draw_plot.py --env h1-hurdle-v0 --optimize frac --set-theta 0.7 --output-file plots/hurdle_frac.svg
pdm run scripts/draw_plot.py --env h1-hurdle-v0 --optimize time_steps --set-theta 0.7 --set-frac 0.2 --output-file plots/hurdle_time_steps.svg
pdm run scripts/draw_plot.py --env h1-hurdle-v0 --optimize K --set-theta 0.7 --set-frac 0.2 --set-time-steps 50 --output-file plots/hurdle_k.svg
