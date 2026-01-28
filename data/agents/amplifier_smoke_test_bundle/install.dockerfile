# uv is already installed in the base.dockerfile

ENV PATH="/root/.cargo/bin:/root/.local/bin:$PATH"

RUN uv tool install git+https://github.com/microsoft/amplifier

RUN amplifier --version

# Register the smoke-test-bundle from the task data
# The bundle files are copied to /project/task_time_data/test-bundle during task setup
RUN amplifier bundle list
