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

## Getting Started

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [prek](https://github.com/j178/prek/blob/master/README.md#installation)

### Setup

Create uv virtual environment and install dependencies:

```bash
uv sync --frozen --all-extras --all-groups
```

Set up git hooks:

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
