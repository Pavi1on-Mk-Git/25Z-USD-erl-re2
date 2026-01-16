import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

HYPERPARAMETERS_GRID = {
    "theta": [0.3, 0.5, 0.7, 0.8],
    "frac": [0.2, 0.5, 0.7, 1.0],
    "time_steps": [50, 200],
    "K": [1, 3],
    "seed": [1, 2, 3],  # not exactly "optimized", but experiment args are prepared analogously
}


def prepare_parser_for_param_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=str, help="Which task to use.", required=True)
    parser.add_argument(
        "--optimize",
        choices=list(HYPERPARAMETERS_GRID.keys()),
        help="Which hyperparameter to optimize.",
        required=True,
    )

    for param in HYPERPARAMETERS_GRID.keys():
        parser.add_argument(
            "--set-" + param.replace("_", "-").lower(),
            type=type(HYPERPARAMETERS_GRID[param][0]),
            help=f"Value of {param} to use. Ignored if {param} is optimized.",
        )

    return parser


def validate_param_args(args: argparse.Namespace):
    should_be_set = True

    for hyperparameter in HYPERPARAMETERS_GRID.keys():
        if args.optimize == hyperparameter:
            should_be_set = False

        is_set = getattr(args, "set_" + hyperparameter.lower()) is not None
        if is_set != should_be_set:
            raise ValueError(
                f"Only hyperparameters before the optimized one must be set explicitly (error for {hyperparameter})."
            )


def parse_args() -> argparse.Namespace:
    parser = prepare_parser_for_param_args()
    parser.add_argument("--num-cpu", type=int, help="Number of CPUs to use per process.", default=1)
    parser.add_argument("--max-processes", type=int, help="Number of processes to run concurrently.", default=1)

    args = parser.parse_args()
    validate_param_args(args)
    return args


@dataclass
class ExperimentID:
    env: str
    theta: float
    frac: float
    time_steps: int
    k: int
    seed: int = 1


def prepare_experiment_ids(args: argparse.Namespace) -> list[ExperimentID]:
    experiment_ids: list[ExperimentID] = []
    for value in HYPERPARAMETERS_GRID[args.optimize]:
        theta = args.set_theta or HYPERPARAMETERS_GRID["theta"][0]
        frac = args.set_frac or HYPERPARAMETERS_GRID["frac"][0]
        time_steps = args.set_time_steps or HYPERPARAMETERS_GRID["time_steps"][0]
        k = args.set_k or HYPERPARAMETERS_GRID["K"][0]
        seed = args.set_seed or HYPERPARAMETERS_GRID["seed"][0]

        match args.optimize:
            case "theta":
                theta = value
            case "frac":
                frac = value
            case "time_steps":
                time_steps = value
            case "K":
                k = value
            case "seed":
                seed = value

        experiment_ids.append(ExperimentID(env=args.env, theta=theta, frac=frac, time_steps=time_steps, k=k, seed=seed))
    return experiment_ids


def experiment_id_to_subprocess_args(id: ExperimentID, args: argparse.Namespace) -> list[str]:
    return [
        "pdm",
        "run",
        "run_re2.py",
        f"-env={id.env}",
        "-disable_cuda",
        "-OFF_TYPE=1",
        "-pr=64",
        "-pop_size=5",
        "-prob_reset_and_sup=0.05",
        f"-theta={id.theta}",
        f"-frac={id.frac}",
        f"-time_steps={id.time_steps}",
        f"-K={id.k}",
        "-gamma=0.99",
        "-TD3_noise=0.2",
        "-EA",
        "-RL",
        "-state_alpha=0.0",
        "-actor_alpha=1.0",
        "-EA_actor_alpha=1.0",
        "-tau=0.005",
        "-seed=1",
        "-logdir=./logs",
        f"-cpu_num={args.num_cpu}",
    ]


def run_process(id: ExperimentID, args: argparse.ArgumentParser):
    arguments = experiment_id_to_subprocess_args(id, args)
    p = subprocess.Popen(arguments, stdout=None, stderr=None)
    p.wait()
    return arguments, p.returncode


def execute_processes(experiment_ids: list[ExperimentID], args: argparse.Namespace):
    with ThreadPoolExecutor(max_workers=args.max_processes) as executor:
        futures = [executor.submit(run_process, id, args) for id in experiment_ids]

        for future in as_completed(futures):
            arguments, return_code = future.result()
            print(f"Process {' '.join(arguments)} finished with exit code {return_code}")


if __name__ == "__main__":
    args = parse_args()
    experiment_ids = prepare_experiment_ids(args)
    execute_processes(experiment_ids, args)
