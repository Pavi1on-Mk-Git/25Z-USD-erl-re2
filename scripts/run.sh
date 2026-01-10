#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 5 ]]; then
    echo "Script requires at least 5 parameters: name theta frac time_steps K [cpu_num]"
fi

name="$1"
theta="$2"
frac="$3"
time_steps="$4"
K="$5"
cpu_num="${6:-1}"

echo "[$name] Running with: $theta $frac $time_steps $K"
pdm run run_re2.py \
    -env="$name" \
    -disable_cuda \
    -OFF_TYPE=1 \
    -pr=64 \
    -pop_size=5 \
    -prob_reset_and_sup=0.05 \
    -time_steps="$time_steps" \
    -theta="$theta" \
    -frac="$frac" \
    -gamma=0.99 \
    -TD3_noise=0.2 \
    -EA \
    -RL \
    -K="$K" \
    -state_alpha=0.0 \
    -actor_alpha=1.0 \
    -EA_actor_alpha=1.0 \
    -tau=0.005 \
    -seed=1 \
    -logdir="./logs" \
    -cpu_num="$cpu_num"
