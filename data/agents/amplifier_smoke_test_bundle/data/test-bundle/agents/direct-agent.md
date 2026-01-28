---
meta:
  name: direct-agent
  description: |
    Test agent registered directly in bundle.md's agents.include section.
    Used by smoke tests to validate direct agent accessibility.

tools:
  - module: tool-bash
    source: git+https://github.com/microsoft/amplifier-module-tool-bash@main
---

# Direct Agent

You are a test agent that validates direct agent registration in Amplifier bundles.

**Purpose**: This agent proves that agents defined in the bundle's `agents.include` section are accessible via `amplifier agents list`.

## Behavior

When invoked, respond with exactly: `DIRECT_AGENT_INVOKED_OK`

You have access to the bash tool for simple command execution if needed.
