# Local source will be copied to /tmp/agent_source by the harness

# Set working directory to the agent source
WORKDIR /tmp/agent_source

# Create virtual environment
RUN uv venv --python 3.11

# Run the install script with UV_SYSTEM_PYTHON unset so it uses the venv
RUN bash -c "unset UV_SYSTEM_PYTHON && bash scripts/install-dev.sh"

# Add the venv to PATH so amplifier command is available
ENV PATH="/tmp/agent_source/.venv/bin:$PATH"

# Return to project directory for task execution
WORKDIR /project

# Verify amplifier is still available
RUN amplifier --version
