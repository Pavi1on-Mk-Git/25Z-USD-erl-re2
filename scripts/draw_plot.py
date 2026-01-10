import argparse
import csv
import json
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from typing import Any

from matplotlib import pyplot as plt


@dataclass
class ExperimentID:
    env: str
    theta: float
    frac: float
    time_steps: int
    k: int


def load_results_csv(results_csv_path: PathLike) -> tuple[list[str], list[str]]:
    best_rewards = []
    num_frames = []

    with open(results_csv_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            best_rewards.append(float(row["best_reward"]))
            num_frames.append(int(row["num_frames"]))

    return num_frames, best_rewards


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("dirnames", nargs="+", help="Which task to use.", required=True)

    return parser.parse_args()


def draw_plot(experiment_ids: list[ExperimentID], legend_labels: list[str], title: str):
    plt.figure(figsize=(10, 6))
    for experiment_id, label in zip(experiment_ids, legend_labels):
        results_csv_path = find_results_csv_path(experiment_id)
        num_frames, best_rewards = load_results_csv(results_csv_path)
        plt.plot(num_frames, best_rewards, linestyle="-", label=label)

    plt.xlabel("Time Steps (1e6)")
    plt.ylabel("Undiscounted Return")
    plt.title(title)

    plt.xlim(0, 1_000_000)

    plt.grid(True)
    plt.legend()

    plt.show()


def get_info(dir_path: Path) -> dict[str, Any]:
    info_path = dir_path / "info.txt"
    with open(info_path, "r") as fh:
        return json.load(fh)


def find_results_csv_path(id: ExperimentID):
    for log_dir in Path("logs").iterdir():
        info = get_info(log_dir)
        if (
            info["env_name"] != id.env
            or info["theta"] != id.theta
            or info["frac"] != id.frac
            or info["time_steps"] != id.time_steps
            or info["K"] != id.k
        ):
            continue

        return log_dir / "results.csv"
    raise FileNotFoundError(f"results file not found for ID: {id}")


if __name__ == "__main__":
    draw_plot(
        [
            ExperimentID(env="h1-walk-v0", theta=0.3, frac=0.2, time_steps=50, k=1),
            ExperimentID(env="h1-walk-v0", theta=0.5, frac=0.2, time_steps=50, k=1),
            # ExperimentID(env="h1-walk-v0", theta=0.7, frac=0.2, time_steps=50, k=1),
            # ExperimentID(env="h1-walk-v0", theta=0.8, frac=0.2, time_steps=50, k=1),
        ],
        ["theta=0.3", "theta=0.5", "theta=0.7", "theta=0.8"],
        "Performance comparison for different theta values",
    )
