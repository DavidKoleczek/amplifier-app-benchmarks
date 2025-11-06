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
uv venv
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

The CLI app has the following options:
- `local_source_path` is the path to your local amplifier development repo to be evaluated. The will use the agent definition found at [./agents/amplifier_next_default](./agents/amplifier_next_default) by default.
- `override_agent_path` optional path to a custom agent definition to use instead of the default one provided.
- `mode` determines which subset of tasks is run.
  - `quick` pulls from eval-recipes two simple tasks: `arxiv_conclusion_extraction` and `cpsc_recall_monitor`
It then uses agent-filter and task-filter to only run the local agent and task. 
The tasks will be pulled directly from the eval-recipes repo by this script and placed in a temporary directory.
- `runs-dir` directory to output results. Defaults to current directory / ".benchmark_results"
- `num_trials` - defaults to 1 for faster iteration.


# Roadmap

- Greater variety of subsets of tasks that can be run quickly for iterative development or a full suite for comprehensive reporting. Currently just supports a quick mode with one hard coded task.
- The ability to define custom tasks specific to Amplifier. Currently we use the ones provided by eval-recipes out of the box.
- Integration with off the shelf benchmarks (such as terminal-bench) for comparison against other agents.
