import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

HYPERPARAMETERS_GRID = {
    "theta": [0.3, 0.5, 0.7, 0.8],
    "frac": [0.2, 0.5, 0.7, 1.0],
    "time_steps": [50, 200],
    "K": [1, 3],
}


def parse_args() -> argparse.Namespace:
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
            type=float,
            help=f"Value of {param} to use. Ignored if {param} is optimized.",
        )
    parser.add_argument("--num_cpu", type=int, help="Number of CPUs to use per process.", default=1)
    parser.add_argument("--max_processes", type=int, help="Number of processes to run concurrently.", default=1)

    return parser.parse_args()


def validate_args(args: argparse.Namespace):
    should_be_set = True

    for hyperparameter in HYPERPARAMETERS_GRID.keys():
        if args.optimize == hyperparameter:
            should_be_set = False

        is_set = getattr(args, "set_" + hyperparameter.lower()) is not None
        if is_set != should_be_set:
            raise ValueError(
                f"Only hyperparameters before the optimized one must be set explicitly (error for {hyperparameter})."
            )


def prepare_subprocess_arguments(args: argparse.Namespace) -> list[list[str]]:
    process_args: list[list[str]] = []
    for value in HYPERPARAMETERS_GRID[args.optimize]:
        theta = args.set_theta or HYPERPARAMETERS_GRID["theta"][0]
        frac = args.set_frac or HYPERPARAMETERS_GRID["frac"][0]
        time_steps = args.set_time_steps or HYPERPARAMETERS_GRID["time_steps"][0]
        k = args.set_k or HYPERPARAMETERS_GRID["K"][0]

        match args.optimize:
            case "theta":
                theta = value
            case "frac":
                frac = value
            case "time_steps":
                time_steps = value
            case "K":
                k = value

        process_args.append(
            [
                "pdm",
                "run",
                "run_re2.py",
                f"-env={args.env}",
                "-disable_cuda",
                "-OFF_TYPE=1",
                "-pr=64",
                "-pop_size=5",
                "-prob_reset_and_sup=0.05",
                f"-theta={theta}",
                f"-frac={frac}",
                f"-time_steps={time_steps}",
                f"-K={k}",
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
        )


def run_process(arguments: list[str]):
    p = subprocess.Popen(arguments, stdout=None, stderr=None)
    p.wait()
    return arguments, p.returncode


def execute_processes(process_args: list[list[str]], max_workers: int):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_process, arguments) for arguments in process_args]

        for future in as_completed(futures):
            arguments, return_code = future.result()
            print(f"Process {' '.join(arguments)} finished with exit code {return_code}")


if __name__ == "__main__":
    args = parse_args()
    validate_args(args)

    process_args = prepare_subprocess_arguments(args)
    execute_processes(process_args, args.max_processes)
