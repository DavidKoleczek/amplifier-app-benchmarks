# amplifier-app-benchmarks

Provide a uvx-installable tool for benchmarking and testing local versions of Amplifier. Although for the most flexible development experience, it is recommended to clone this app locally so that you can give your agent the context on how to best use this app.

The tool is a custom wrapper around [eval-recipes](https://github.com/microsoft/eval-recipes)'s benchmarking capability, preconfigured for Amplifier.


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
uv pip install -e .
uv run run_benchmarks \
    --local_source_path /path/to/local/amplifier-development/ \
    --runs-dir ".benchmark_results/" \
    --mode quick
```


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


# Architecture

A Python Click CLI app to implement a custom version of the eval-recipes' benchmarking script found [here](https://github.com/DavidKoleczek/eval-recipes/blob/main/scripts/run_benchmarks.py).

## CLI Options

The CLI app has the following options:
- `local_source_path` is the path to your local amplifier development repo to be evaluated. This will use the agent definition found at [./agents/amplifier_next_default](./agents/amplifier_next_default) by default.
- `override_agent_path` optional path to a custom agent definition to use instead of the default one provided.
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
- `max_parallel_tasks` maximum number of tasks to run in parallel. If provided, this overrides the default set by the mode.


# Roadmap

- Integration with off the shelf benchmarks (such as terminal-bench) for comparison against other agents.
