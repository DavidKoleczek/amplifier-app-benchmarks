<h1 align="center">
    Amplifier App Benchmarks
</h1>
<p align="center">
    <p align="center">Testing and Benchmarking Amplifier at scale.
    </p>
</p>
<p align="center">
    <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv"></a>
    <a href="https://github.com/astral-sh/ty"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json" alt="ty"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</p>

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Install [Docker Desktop](https://docs.docker.com/desktop/) for work on systems running Windows* or [Docker Engine](https://docs.docker.com/engine/install/ubuntu/) on setups like WSL 2.
  - After installing Docker Engine on WSL 2, ensure your user has docker permissions by running:
    - `sudo usermod -aG docker $USER`
    - `newgrp docker`
- The Claude Agent SDK which requires setting up [Claude Code](https://docs.claude.com/en/docs/claude-code/overview)
- [`ANTHROPIC_API_KEY`](https://platform.claude.com/docs/en/get-started) for the Claude Agent SDK.
- [`OPENAI_API_KEY`](https://platform.openai.com/api-keys) if using agent continuation (see parameters below, or running tasks that requires it as a dependency).

\* All features may not currently work on Windows due to Claude Agent SDK limitations.


## Usage

### (Recommended) Clone locally

Cloning locally is currently recommended because it will give you access to the provided evaluation configurations, agents, and tasks.
See the section [Provided Run Configurations](#provided-run-configurations) for more details on pre-configured evaluation configurations.

```bash
git clone https://github.com/DavidKoleczek/amplifier-app-benchmarks
cd amplifier-app-benchmarks

uv run amplifier-benchmarks run --benchmark data/benchmarks/sample.yaml
```

### Install as a tool

```bash
uv tool install "git+https://github.com/DavidKoleczek/amplifier-app-benchmarks"
amplifier-benchmarks run --benchmark path/to/benchmark.yaml --agents-dir path/to/agents --tasks-dir path/to/tasks
```

### Run directly with uvx

```bash
uvx --from "git+https://github.com/DavidKoleczek/amplifier-app-benchmarks" amplifier-benchmarks run \
    --benchmark path/to/benchmark.yaml \
    --agents-dir path/to/agents \
    --tasks-dir path/to/tasks
```

### CLI Options

```
amplifier-benchmarks run [OPTIONS]

Options:
  --benchmark PATH         Path to a benchmark definition YAML file. (Required)
  --agents-dir PATH        Directory containing agent configurations. Defaults to data/agents.
  --tasks-dir PATH         Directory containing task definitions. Defaults to data/tasks.
  --output-dir PATH        Directory to store benchmark results. Creates timestamped dir if not provided.
  --max-parallel INTEGER   Maximum number of parallel jobs (default: 12).
```

### Provided Run Configurations

Three benchmark configurations are provided in [data/benchmarks](data/benchmarks):

| Configuration | Description |
|---------------|-------------|
| `sample.yaml` | Quick test with 3 simple tasks - use for validating setup |
| `full.yaml` | Complete benchmark run |
| `regression.yaml` | Amplifier CLI regression tests (provider response, tool execution, agent delegation) |


## Development

### Setup

Create uv virtual environment and install dependencies:

```bash
uv sync --frozen --all-extras --all-groups
```

Set up git hooks (requires [prek](https://github.com/j178/prek/blob/master/README.md#installation)):

```bash
prek install
```

To update dependencies (updates the lock file):

```bash
uv sync --all-extras --all-groups
```

Run formatting, linting, and type checking in one command:

```bash
uv run ruff format && uv run ruff check --fix && uv run ty check
```

### Further Information

[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)
