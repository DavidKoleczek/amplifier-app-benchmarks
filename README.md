# amplifier-app-benchmarks

Provide a uvx-installable tool for benchmarking and testing local versions of Amplifier. Although for the most flexible development experience, it is recommended to clone this app locally so that you can give your agent the context on how to best use this app.

The tool is a custom wrapper around [eval-recipes](https://github.com/microsoft/eval-recipes)'s benchmarking capability, preconfigured for Amplifier.

We also provide an experimental wrapper around [Harbor](https://harborframework.com/docs/getting-started#installation) to facilitate running industry benchmarks like terminal-bench 2.0. It is detailed at the end.


## Quick Start

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Docker](https://docs.docker.com/engine/install/ubuntu/)
  - After installing, ensure your user has docker permissions by running:
    - `sudo usermod -aG docker $USER`
    - `newgrp docker`
- Claude Agent SDK which requires [Claude Code](https://docs.claude.com/en/docs/claude-code/overview)
- ANTHROPIC_API_KEY for the Claude Agent SDK.
- OPENAI_API_KEY since some tasks leverage eval-recipes that require OpenAI models.

### Run from GitHub (uvx)

```bash
uvx --from git+https://github.com/DavidKoleczek/amplifier-app-benchmarks \
    run_benchmarks \
    --local_source_path /path/to/local/amplifier-development/ \
    --runs-dir ".benchmark_results/" \
    --mode quick
```

### Run from Local Clone

```bash
git clone https://github.com/DavidKoleczek/amplifier-app-benchmarks.git
cd amplifier-app-benchmarks
uv venv
uv pip install -e .
# harbor requires openai<1.100.0 but eval-recipes requires openai>=2.1, so we install harbor without deps and add them manually
uv pip install harbor==0.1.18 --no-deps
uv pip install "jinja2>=3.1.6" "pydantic>=2.11.7" "shortuuid>=1.0.13" "typer>=0.16.0" "requests>=2.32.4" "pyyaml>=6.0.2" "rich>=14.1.0" "toml>=0.10.2" "tenacity>=9.1.2" "python-dotenv>=1.1.1" "litellm>=1.79.0" "dirhash>=0.5.0" "e2b>=2.4.2" "modal>=1.2.1" "datasets>=4.4.1" "runloop-api-client>=0.64.0" "daytona==0.112.2"
uv run run_benchmarks \
    --local_source_path /path/to/local/amplifier-development/ \
    --runs-dir ".benchmark_results/" \
    --mode sanity_check
```

### Run with Predefined Agent (no local source needed)

```bash
uv run run_benchmarks \
    --agent amplifier_v2_toolkit \
    --runs-dir ".benchmark_results/" \
    --mode sanity_check
```


### Creating Custom Agents and Tasks

See [docs/CREATE_BENCHMARK_TASK.md](docs/CREATE_BENCHMARK_TASK.md) and [docs/CREATE_SEMANTIC_TEST.md](docs/CREATE_SEMANTIC_TEST.md)


## Interpreting Results

Results are saved to timestamped directories in `runs-dir` (defaults to `.benchmark_results/`). Each run contains:

- **`benchmark_report.html`** - Interactive HTML report with scores, charts, and detailed breakdowns
- **`CONSOLIDATED_REPORT_amplifier.md`** - Executive summary analyzing failure patterns and root causes across all tasks
- **`{agent}_{task}/aggregated_results.json`** - Per-task statistics (mean/median/std scores, trial results)
- **`{agent}_{task}/trial_{N}/`** - Individual trial logs:
  - `test_results.json` - Score and test metadata
  - `agent_output.log` - Complete agent execution logs captured from the agent running within Docker
  - `FAILURE_REPORT_trial_{N}.md` - Detailed failure analysis (only generated for tasks scoring <85%)

Scores range from 0-100%. The consolidated report categorizes failures and provides actionable insights for agent improvements.

## `run_benchmarks` CLI Options

The `run_benchmarks` command has the following options:
- `local_source_path` path to your local amplifier development repo to be evaluated. Uses the agent definition at [./agents/amplifier_next_default](./agents/amplifier_next_default). **Mutually exclusive with `--agent`.**
- `agent` use a predefined bundled agent that pulls from git (e.g., `amplifier_v2_toolkit`). **Mutually exclusive with `--local_source_path`.**
- `override_agent_path` optional path to a custom agent definition (only with `--local_source_path`).
- `mode` determines which tasks are run and execution defaults.
  - **Predefined modes:**
    - `sanity_check`: 2 simple tasks (1 trial, 2 parallel) - Quick validation
    - `quick`: 5 representative tasks (2 trials, 10 parallel, ~1 hour) - Default mode
    - `full`: 14 tasks (5 trials, 20 parallel, many hours) - Comprehensive evaluation
  - **Custom task modes:**
    - Note: for now, the details of what a custom task should be is only available in the eval-recipes library
    - `quick+/path/to/tasks`: Adds custom tasks to quick mode's eval-recipes tasks
    - `/path/to/tasks`: Runs only custom tasks (1 trial, 5 parallel default)

  Predefined modes pull tasks from the eval-recipes repo. Custom tasks are copied from your local directory.
- `runs-dir` directory to output results. Defaults to current directory / ".benchmark_results"
- `num_trials` number of times to try each task, defaults to 1 for faster iteration. If provided, this overrides the amount set by the mode
- `max_parallel_trials` maximum number of trials to run in parallel. If provided, this overrides the default set by the mode.
- `continuation-provider` LLM provider for agent continuation - `openai`, `azure_openai`, or `none` to disable. Defaults to `openai`.
- `continuation-model` model to use for agent continuation decisions - `gpt-5` or `gpt-5.1`. Defaults to `gpt-5`.
- `report-score-threshold` minimum score threshold to skip report generation (reports generated for scores below this). Defaults to 85.0.


## Run Terminal-Bench with Harbor

Run the [terminal-bench@2.0](https://github.com/laude-institute/harbor) benchmark using Harbor. This runs a **predetermined version of Amplifier** (from `microsoft/amplifier@next` with `amplifier-collection-toolkit@main`) using the `toolkit:toolkit-dev` profile and `claude-sonnet-4-5-20250929` model by default.

**Note:** Harbor must be configured separately. See the [Harbor GitHub repository](https://github.com/laude-institute/harbor) and [Harbor documentation](https://harborframework.com/docs/getting-started) for installation instructions.

```bash
# Run all 89 terminal-bench tasks with multiple concurrent trials
uv run run_harbor --n-concurrent 2 --n-attempts 3

# Run a specific task 
uv run run_harbor --task prove-plus-comm 

# List available datasets
uv run run_harbor --list-datasets

# List tasks in terminal-bench
uv run run_harbor --list-tasks

# Specify output directory
uv run run_harbor --jobs-dir ./my_results
```

**Harbor CLI Options:**
- `--dataset` / `-d`: Benchmark dataset (default: `terminal-bench`)
- `--version` / `-v`: Dataset version (default: `2.0`)
- `--task` / `-t`: Specific task to run (omit for all tasks)
- `--model` / `-m`: LLM model for the agent (default: `claude-sonnet-4-5-20250929`)
- `--n-concurrent` / `-n`: Number of concurrent trials (default: `1`)
- `--n-attempts` / `-k`: Number of attempts per task (default: `1`)
- `--jobs-dir` / `-o`: Output directory (default: `./harbor_jobs`)
- `--list-datasets`: List available datasets from Harbor registry
- `--list-tasks`: List tasks in the selected dataset
