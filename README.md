# StudyPilot — Agentic Study Planner

StudyPilot is a local web app that uses a transparent, rule-based agent to prioritise study tasks, allocate study hours, and verify whether work fits within daily limits and deadlines.

## Features
- Add, remove, and edit study tasks in the browser.
- Prioritise by importance, deadline urgency, and remaining workload.
- Allocate sessions within a daily study-hour limit.
- Verify daily workload and report unscheduled hours.
- Update completed hours and rerun the agent to replan.
- Print or save the generated plan.

## Requirements
- Python 3.10 or newer
- Internet connection for the initial Flask installation
- A modern browser

## Run on Windows
1. Install Python from https://www.python.org/downloads/ if needed. During installation, select **Add Python to PATH**.
2. Extract this project ZIP.
3. Open the extracted `StudyPilot-Agent` folder in File Explorer.
4. Click the address bar, type `cmd`, and press Enter.
5. Run:

```bat
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py app.py
```

6. Open http://127.0.0.1:5000 in your browser.
7. Keep the Command Prompt window open while using the app. Press Ctrl+C to stop it.

If `py` is not recognised, try replacing `py` with `python`.

## Agent workflow
1. Receive tasks, deadlines, estimated hours, completed hours, and importance.
2. Calculate a priority score.
3. Invoke the scheduling tool to allocate remaining work.
4. Verify the daily hour limit and identify unscheduled work.
5. Present the schedule and any warning to the user.

## Architecture
See [`architecture.md`](architecture.md).

## Limitations
- Rule-based agent; it does not use an LLM or external AI API.
- The greedy scheduler is a simple heuristic and does not guarantee a globally optimal schedule.
- The application does not persist tasks after the page is refreshed.
- It runs locally and is not publicly deployed by default.

## Testing checklist
- Generate a plan using the default example tasks.
- Add and remove a task.
- Mark some hours as completed and regenerate.
- Set the daily study limit low enough that some work cannot be scheduled.
- Confirm the app reports unscheduled work and the workload check passes.
