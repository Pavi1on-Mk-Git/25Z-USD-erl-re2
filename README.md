# USD - ERL-Re2

### Docker setup guide

Build system image:
```bash
docker build -t usd .
```
Run the built image:
```bash
docker run -it usd
```

*Note: All of the experimental results created in a Docker environment need to be copied out of it before terminating the process, as the container's state is not preserved between separate runs.*

### Local installation guide

In order to install the project one can simply repeat the steps specified in `.dockerfile` locally on their machine, with `/root` substituted by the user's home directory.

It may be necessary to add the path to NVIDIA libraries to `LD_LIBRARY_PATH` (i.e. `/usr/lib/nvidia`).

### Reproducing the experiments

- `./scripts/run_all.sh` - runs all the experiments
- `./scripts/draw_all.sh` - produces all the plots of experimental results (assuming `./logs` contains experiment results)

Additionally, each individual experiment can be reproduced by running `./scripts/run.sh` with appropriate parameters.
