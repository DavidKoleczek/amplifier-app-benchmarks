# amplifier-app-benchmarks

Provide a uvx-installable tool for benchmarking Amplifier.

Currently the tool will be a wrapper around [eval-recipes](https://github.com/microsoft/eval-recipes)'s benchmarking capability preconfigured for running evaluations of Amplifier.


# Quick Start

## Prerequisites

- uv
- `ANTHROPIC_API_KEY=sk-ant-...` set as an env var.
- `OPENAI_API_KEY=sk-... ` set as an env var.


```bash
uvx --from git+https://github.com/DavidKoleczek/amplifier-app-benchmarks run_benchmarks --mode quick
```


# Architecture

Uses a Python Click CLI app to implement the eval-recipes benchmarking script of eval-recipes: https://github.com/DavidKoleczek/eval-recipes/blob/main/scripts/run_benchmarks.py
The CLI app has the following options:
- `mode` - Currently only `quick` which pulls the https://github.com/DavidKoleczek/eval-recipes/tree/main/data/agents/amplifier_v2 agent and the https://github.com/DavidKoleczek/eval-recipes/tree/main/data/tasks/arxiv_conclusion_extraction task as the default of what will be run. It then uses agent-filter and task-filter to only run that agent and task. The agent and task will need to be pulled directly from the eval-recipes repo by this script and placed in a temporary directory, setting agents_dir and tasks_dir accordingly.
- `runs-dir` directory to output results. Defaults to current directory / ".benchmark_results"
- `num_trials` - defaults to 1


# Roadmap

- Greater variety of subsets of tasks that can be run quickly for iterative development or a full suite for comprehensive reporting. Currently just supports a quick mode with one hard coded task.
- The ability to define custom tasks specific to Amplifier. Currently we use the ones provided by eval-recipes out of the box.
- Integration with off the shelf benchmarks (such as terminal-bench) for comparison against other agents.
