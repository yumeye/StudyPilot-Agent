from datetime import date, timedelta
from flask import Flask, render_template, request

app = Flask(__name__)

def priority_score(task, today):
    days_left = max(0, (task["deadline"] - today).days)
    urgency = 10 / (days_left + 1)
    remaining = max(0, task["hours"] - task["completed"])
    return task["importance"] * 2 + urgency + remaining * 0.2

def schedule_tool(tasks, daily_hours, today):
    schedule = {}
    remaining = {
        t["name"]: max(0.0, t["hours"] - t["completed"])
        for t in tasks
    }
    last_day = max((t["deadline"] for t in tasks), default=today)

    for offset in range(max(0, (last_day - today).days) + 1):
        current_day = today + timedelta(days=offset)
        available = daily_hours
        schedule[current_day] = []
        candidates = sorted(
            [t for t in tasks
             if t["deadline"] >= current_day and remaining[t["name"]] > 0],
            key=lambda t: priority_score(t, today),
            reverse=True
        )
        for task in candidates:
            if available <= 0:
                break
            session = min(remaining[task["name"]], available)
            if session > 0:
                schedule[current_day].append((task["name"], round(session, 2)))
                remaining[task["name"]] = round(remaining[task["name"]] - session, 2)
                available = round(available - session, 2)
    return schedule, remaining

def verify_plan(schedule, remaining, daily_hours):
    valid = all(sum(hours for _, hours in sessions) <= daily_hours + 1e-9
                for sessions in schedule.values())
    unresolved = {name: hours for name, hours in remaining.items() if hours > 0}
    return valid, unresolved

def run_agent(tasks, daily_hours):
    today = date.today()
    print("STUDYPILOT AGENT: starting")
    print("Goal: create a feasible study plan")
    print("Action: prioritising subjects")
    ranked = sorted(tasks, key=lambda t: priority_score(t, today), reverse=True)
    for task in ranked:
        task["score"] = priority_score(task, today)
        print(f"  {task['name']}: priority score {task['score']:.2f}")
    print("Action: invoking scheduling tool")
    schedule, remaining = schedule_tool(tasks, daily_hours, today)
    print("Action: verifying schedule")
    valid, unresolved = verify_plan(schedule, remaining, daily_hours)
    print(f"Verification: daily workload valid = {valid}")
    if unresolved:
        print("Unscheduled work:", unresolved)
    else:
        print("Verification: all remaining work scheduled before deadlines")
    return schedule, unresolved, ranked, valid

@app.route("/", methods=["GET", "POST"])
def index():
    today = date.today()
    results = None
    error = None
    initial_tasks = [
        {"name": "Mathematics", "deadline": (today + timedelta(days=2)).isoformat(),
         "hours": "4", "completed": "0", "importance": "5"},
        {"name": "Physics", "deadline": (today + timedelta(days=4)).isoformat(),
         "hours": "3", "completed": "0", "importance": "4"},
        {"name": "Programming", "deadline": (today + timedelta(days=3)).isoformat(),
         "hours": "5", "completed": "1", "importance": "5"},
    ]
    if request.method == "POST":
        try:
            daily_hours = float(request.form.get("daily_hours", "3"))
            if not 0.25 <= daily_hours <= 24:
                raise ValueError("Daily study hours must be between 0.25 and 24.")
            names = request.form.getlist("name[]")
            deadlines = request.form.getlist("deadline[]")
            hours_list = request.form.getlist("hours[]")
            completed_list = request.form.getlist("completed[]")
            importance_list = request.form.getlist("importance[]")
            tasks = []
            for i, name in enumerate(names):
                name = name.strip()
                if not name:
                    continue
                deadline = date.fromisoformat(deadlines[i])
                hours = float(hours_list[i])
                completed = float(completed_list[i])
                importance = int(importance_list[i])
                if deadline < today:
                    raise ValueError(f"Deadline for {name} cannot be in the past.")
                if hours <= 0 or completed < 0 or completed > hours:
                    raise ValueError(f"Check total/completed hours for {name}.")
                if importance not in range(1, 6):
                    raise ValueError("Importance must be between 1 and 5.")
                tasks.append({"name": name, "deadline": deadline, "hours": hours,
                              "completed": completed, "importance": importance})
            if not tasks:
                raise ValueError("Add at least one subject/task.")
            schedule, unresolved, ranked, valid = run_agent(tasks, daily_hours)
            results = {
                "schedule": [(day, sessions) for day, sessions in schedule.items()],
                "unresolved": unresolved, "ranked": ranked, "valid": valid,
                "daily_hours": daily_hours,
                "total_remaining": round(sum(max(0, t["hours"]-t["completed"]) for t in tasks), 2)
            }
        except (ValueError, IndexError) as exc:
            error = str(exc)
    return render_template("index.html", today=today.isoformat(),
                           tasks=initial_tasks, results=results, error=error)

if __name__ == "__main__":
    print("\nStudyPilot is starting...")
    print("Open http://127.0.0.1:5000 in your browser.")
    app.run(host="127.0.0.1", port=5000, debug=False)
