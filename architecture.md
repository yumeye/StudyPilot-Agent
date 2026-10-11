# StudyPilot — Development Schema & Architecture

## 1. Project objective
StudyPilot is a browser-based study planning application. It accepts tasks, deadlines, estimated hours, completed hours, importance ratings, and daily availability. Its rule-based agent prioritises tasks, allocates sessions, verifies the schedule, and reports work that remains unscheduled.

## 2. Agent workflow
1. **Observe:** collect and validate task details and daily study availability.
2. **Track progress:** calculate remaining hours = estimated hours − completed hours.
3. **Decide:** score and rank tasks by importance, deadline urgency, and remaining workload.
4. **Act:** call the scheduling tool to allocate sessions within the daily limit.
5. **Verify:** check daily workload and identify unscheduled work.
6. **Respond/replan:** show the plan and warnings; the user can update progress and rerun the agent.

## 3. Priority scoring
`score = 2 × importance + 10 / (days_until_deadline + 1) + 0.2 × remaining_hours`

This is a transparent heuristic, not an LLM-generated score.

## 4. Technology
- Python 3
- Flask
- HTML, CSS, JavaScript
- Local browser interface
- No external AI API or database required

## 5. Components
- `app.py`: Flask routes, priority scoring, scheduling, verification, agent controller.
- `templates/index.html`: input form and results interface.
- `static/style.css`: responsive styling.
- `requirements.txt`: dependency declaration.
- `README.md`: installation and usage guide.

## 6. Validation
The verification tool checks that no day's scheduled hours exceed the daily limit and lists tasks with remaining unscheduled work.

## 7. Limitations
- Rule-based rather than LLM-powered.
- Greedy scheduler; it does not guarantee a globally optimal plan.
- No persistent database or calendar integration.
- Local app; not deployed publicly by default.

## 8. Test checklist
- Generate a plan using sample tasks.
- Add/remove tasks.
- Change completed hours and regenerate.
- Reduce daily availability to test unscheduled-work warnings.
- Check that daily allocations respect the configured limit.
