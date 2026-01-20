# Development

## Git Hooks

This project uses [prek](https://github.com/j178/prek) for git hooks. See [`.pre-commit-config.yaml`](../.pre-commit-config.yaml) for the full configuration.

Run all hooks manually:

```bash
prek run --all-files
```


## Code Quality

Format code:

```bash
uv run ruff format
```

Lint code:

```bash
uv run ruff check --fix
```

Type check:

```bash
uv run ty check
```
