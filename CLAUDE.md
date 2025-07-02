# Running project

- use `nohup textual serve src/dromadaire/__main__.py > /dev/null 2>&1 &` which will load the app in the browser in the background, don't wait for the command to complete, move on to the next step
- navigate to http://localhost:8000 to see the browser version of the app

# General workflow

- inspect requirements carefully and come up with the plan
- proceed with the execution
- when necessary, rerun the app, take a screenshot, inspect it and decide if any additional changes are required
- after making changes to the code, run checks and clean things up in necessary using `uv run ruff check`