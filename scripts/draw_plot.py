import argparse
import csv
import json
from os import PathLike
from pathlib import Path
from typing import Any

import numpy as np
from compare_hyperparameter import (
    HYPERPARAMETERS_GRID,
    ExperimentID,
    prepare_experiment_ids,
    prepare_parser_for_param_args,
    validate_param_args,
)
from matplotlib import pyplot as plt


def parse_args() -> argparse.Namespace:
    parser = prepare_parser_for_param_args()
    parser.add_argument("--smoothing-sigma", type=float, help="Sigma for Gaussian smoothing of the plot.", default=None)
    parser.add_argument("--output-file", type=str, help="File to write plto to. Default: display.", default=None)

    args = parser.parse_args()
    validate_param_args(args)
    return args


def draw_plot(
    experiment_ids: list[ExperimentID],
    legend_labels: list[str],
    title: str,
    smoothing_sigma: float | None = None,
):
    plt.figure(figsize=(6, 4))
    for experiment_id, label in zip(experiment_ids, legend_labels):
        results_csv_path = find_results_csv_path(experiment_id)
        num_frames, best_rewards = load_results_csv(results_csv_path)
        auc = np.trapezoid(best_rewards, num_frames)
        best_rewards = smoothen(num_frames, best_rewards, smoothing_sigma)
        plt.plot(num_frames, best_rewards, linestyle="-", label=f"{label} (AUC={auc:.3e})")

    plt.xlabel("Time Steps (1e6)")
    plt.ylabel("Undiscounted Return")
    plt.title(title)

    plt.xlim(0, 1_000_000)

    plt.grid(True)
    plt.legend()

    if args.output_file is not None:
        plt.savefig(args.output_file, bbox_inches="tight")
    else:
        plt.show()


def find_results_csv_path(id: ExperimentID):
    for log_dir in Path("logs").iterdir():
        info = get_info(log_dir)
        if (
            info["env_name"] != id.env
            or info["theta"] != id.theta
            or info["frac"] != id.frac
            or info["time_steps"] != id.time_steps
            or info["K"] != id.k
            or info["seed"] != id.seed
        ):
            continue

        return log_dir / "results.csv"
    raise FileNotFoundError(f"results file not found for ID: {id}")


def get_info(dir_path: Path) -> dict[str, Any]:
    info_path = dir_path / "info.txt"
    with open(info_path, "r") as fh:
        return json.load(fh)


def load_results_csv(results_csv_path: PathLike) -> tuple[list[str], list[str]]:
    best_rewards = []
    num_frames = []

    with open(results_csv_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            best_rewards.append(float(row["best_reward"]))
            num_frames.append(int(row["num_frames"]))

    return num_frames, best_rewards


def smoothen(num_frames: list[int], best_rewards: list[float], sigma: float | None) -> list[float]:
    if sigma is None:
        return best_rewards

    num_frames = np.array(num_frames)
    best_rewards = np.array(best_rewards)
    rewards_smooth = np.zeros_like(best_rewards, dtype=float)

    for i in range(len(num_frames)):
        weights = np.exp(-0.5 * ((num_frames - num_frames[i]) / sigma) ** 2)
        rewards_smooth[i] = np.sum(weights * best_rewards) / np.sum(weights)

    return rewards_smooth


def prepare_legend(optimized_param: str):
    values = HYPERPARAMETERS_GRID[optimized_param]
    return [f"{optimized_param}={value}" for value in values]


if __name__ == "__main__":
    args = parse_args()
    experiment_ids = prepare_experiment_ids(args)
    legend = prepare_legend(args.optimize)
    draw_plot(
        experiment_ids,
        legend,
        f"Performance comparison for different {args.optimize} values",
        smoothing_sigma=args.smoothing_sigma,
    )
