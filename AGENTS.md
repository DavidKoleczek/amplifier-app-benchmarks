@README.md

## Changing Configuration of the Local Agent

The default configuration of the agent makes some assumptions about the `local_source_path` and other settings. It is available at [./agents/amplifier_next_default](./agents/amplifier_next_default).
The assumptions are:
- The command to kick start the agent per task is at [./agents/amplifier_next_default/command_template.txt](./agents/amplifier_next_default/command_template.txt)
- The installation script assumes that the repo contains a `scripts/install-dev.sh` script that can install the agent in a development mode. 
- It will automatically ignore any gitignored files from the local source path when building the Docker image.


### Creating a Local Agent Variant

1. Create a new agent directory (e.g., `data/agents/your_agent_local/`)
2. Add `agent.yaml` with `local_source_path` pointing to your local source:
   ```yaml
   local_source_path: /absolute/path/to/your/agent/source
   required_env_vars:
     - API_KEY
   ```
3. Create `install.dockerfile` that installs from `/tmp/agent_source/` (where source is automatically copied)
4. Copy or create `command_template.txt`


### How It Works

1. Harness validates `local_source_path` exists
2. Collects files, respecting `.gitignore` if present (otherwise excludes `.git`, `.venv`, `__pycache__`, etc.)
3. Adds files to Docker build context as `agent_source/`
4. Copies `agent_source` to `/tmp/agent_source/` in container
5. Your `install.dockerfile` installs from there. This dockerfile should install the agent so that it is globally available. The commands will run in `/project/`, not where the agent's files are.
6. Image is rebuilt each run, capturing your latest changes


# Troubleshooting

If you run into issues, please double check and think hard in these areas:
- Make sure the prerequisites are correctly installed and configured. See the README. 
Common errors may be due to Docker/installs, missing API keys, or misconfiguration. For example using Azure OpenAI within Docker requires additional setup.
- Double check paths provided to the CLI are correct.
- Correctly installing an agent from local source can be finicky. Double check that you followed the correct instructions and made any special considerations for the agent running within Docker.
- Lastly, this app is in active development. Be patient and reach out to the maintainer for help!
- For deeper troubleshooting, look at the source code of the eval-recipes package. The llms.txt is available at https://github.com/microsoft/eval-recipes/blob/main/llms.txtt and the repo is at https://github.com/microsoft/eval-recipes


# Common Questions

Q: How can I compare the performance of different agents?
A: Currently, the recommendation is to point the `local_source_path` to different local versions of Amplifier that have different agent definitions checked out.
In the future, we may add support for specifying multiple agents to compare in a single run.

Q: How can I specify different or my own tasks to run?
A: This is not currently supported without code changes to the app, but is planned soon.

Q: Why is it taking so long?
A: Each task not only runs the agent solving an often long running problem, but then runs a semantic test which is its own agent that evaluates the output and takes time to do its work. Each task per trial is expected to take upwards of 20 minutes or more.
