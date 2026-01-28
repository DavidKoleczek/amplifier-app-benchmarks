---
bundle:
  name: smoke-test-bundle
  version: 1.0.0
  description: Self-contained bundle for validating bundle composition mechanisms

includes:
  # Test transitive agent and context inclusion via behavior
  - bundle: smoke-test-bundle:behaviors/contributing-behavior.yaml

# Explicit tool selection - only these tools should be mounted
# This enables negative testing (tool-web, tool-task should NOT appear)
tools:
  - module: tool-filesystem
    source: git+https://github.com/microsoft/amplifier-module-tool-filesystem@main
  - module: tool-bash
    source: git+https://github.com/microsoft/amplifier-module-tool-bash@main

# Direct agent registration
agents:
  include:
    - smoke-test-bundle:direct-agent

# Direct context inclusion (via YAML frontmatter)
# Note: @mentions in markdown body are NOT resolved - use context.include instead
context:
  include:
    - smoke-test-bundle:context/direct-context.md

# Session config with required orchestrator, context manager, and logging
session:
  orchestrator:
    module: loop-basic
    source: git+https://github.com/microsoft/amplifier-module-loop-basic@main
  context:
    module: context-simple
    source: git+https://github.com/microsoft/amplifier-module-context-simple@main

# Hooks for session logging (required for test verification)
hooks:
  - module: hooks-logging
    source: git+https://github.com/microsoft/amplifier-module-hooks-logging@main
---

# Bundle Composition Test Bundle

Self-contained test bundle for validating Amplifier bundle composition mechanisms.

## What This Bundle Tests

1. **Direct Agent**: `direct-agent` registered in this bundle's `agents.include`
2. **Transitive Agent**: `behavior-agent` contributed by `contributing-behavior.yaml`
3. **Tool Selection (Positive)**: `tool-filesystem` and `tool-bash` should be mounted
4. **Tool Selection (Negative)**: `tool-web`, `tool-task`, `tool-search` should NOT be mounted
5. **Direct Context**: Token `BUNDLE_DIRECT_CONTEXT_ALPHA` from `context.include` in frontmatter
6. **Transitive Context**: Token `BEHAVIOR_TRANSITIVE_CONTEXT_BETA` from behavior's `context.include`
