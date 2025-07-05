# Running project

- this project uses `uv` to manage dependencies, run commands etc:
  - Claude must add dependencies using uv
  - Claude must run `uv pip install -e .`
- use `nohup textual serve src/dromadaire/__main__.py > /dev/null 2>&1 &` which will load the app in the browser in the background, don't wait for the command to complete, move on to the next step
- navigate to http://localhost:8000 to see the browser version of the app

# General workflow

- inspect requirements carefully and come up with the plan
- proceed with the execution
- when necessary, rerun the app, take a screenshot, inspect it and decide if any additional changes are required
- if you need inspiration/help with particular patterns/tasks, you can get relevant help by running `python tools/inspire.py "YOUR QUESTION HERE"`
- after making changes to the code, run checks and clean things up in necessary using `uv run ruff check`

User might ask you questions related to Textualize framework docs or one of the example projects that we are using for inspiration. Also, user might ask you to copy certain
functionality from one of the sample apps. When this happens, use the following command to gather required information and code snippets before generating code or providing responses:

```
uv run tools/gemini.py <docs|dolphie|harlequin|posting> "<question>"
```

# Things Claude MUST NOT DO

- inspect `kb` dir and its subdirectories