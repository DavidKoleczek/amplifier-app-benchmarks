The user has optionally provided a description of a task they want or a bunch of data or something in-between.
It is your job to create a new benchmark task for them based on whatever they have provided. The following outlines the process which you should make a todo list for yourself and then execute it.

Look at `/home/dkoleczek/repos/amplifier-dev-dave/amplifier-app-benchmarks/custom_tasks_example/system_info_utility` for an example of a simple task

FILL OUT TEMPLATE:
1. Start by filling out the `instructions.txt`. This will be the "user's" description for the agent describing what they want to have done.
   1. Remember, these instructions are meant to imitate **real** users who might not be engineers or experts in the field or AI. However, do not add extra fluff - users are actually usually pretty concise and leave out details. Create a todo-list item to self-reflect on your initial draft of instructions to make it more user-like. If the user provided something that already looks like instructions don't make much if any changes to it.
2. Next, update the `setup.dockerfile`. This should **only** be updated if the user has specified a specific dependency that the agent could not determine to install itself. If anything, keep this file as minimal as possible. Don't forget to remove the placeholder comment and add to a todo about NOT adding a placeholder comment.
3. Update `task.yaml` with the required environment variables, task info, and, for now, leave the `test_command` as the default.
4. Leave the `test.py` alone as a template for now. DO NOT make changes to it at this time. At the end, let the user know that they can use the command /create-semantic-tests to create semantic tests for this new task.
