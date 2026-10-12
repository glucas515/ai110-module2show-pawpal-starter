# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule
08:00 - Feeding (Mochi) [high, 10 min]
08:10 - Morning walk (Mochi) [high, 30 min]
08:40 - Litter box (Whiskers) [medium, 15 min]
Skipped (not enough time)
Grooming (Whiskers) [low, 45 min]
```



## 🧪 Testing PawPal+

Run the full test suite from the project root:



```bash
python -m pytest
```

The tests in `tests/test_pawpal.py` cover:

- **Task completion and adding tasks:** `mark_complete()` changes a task's status, and `Pet.add_task()` increases the pet's task count.
- **Sorting:** `sort_by_time()` returns tasks in chronological order, with untimed tasks last.
- **Recurrence:** completing a daily task creates one new task due tomorrow, completing it twice doesn't create a duplicate, and a one-time task doesn't recur.
- **Conflict detection:** `detect_conflicts()` warns when two pending tasks share a time, and stays quiet for different times or completed tasks.

Test output:

```
PS C:\Users\norai\pawPal\ai110-module2show-pawpal-starter> python -m pytest
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\norai\pawPal\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 7 items

tests\test_pawpal.py .......                                             [100%]

============================== 7 passed in 0.03s ==============================

```

**Confidence level:** ★★★★☆ (4/5)

All 7 tests pass and they cover the sorting, recurrence and conflict-detection logic. I'm not at 5 stars because `generate_plan()` (exact fits, skipped tasks, empty schedule), filtering and input validation have no unit tests yet. I checked the plan through the `main.py` demo instead.


## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

|        Feature                          Method(s)                               Notes 
|------------------------------|--------------------------------|----------------------------------|
|Sorting                   |       Scheduler.sort_by_time()      |    Orders tasks by `preferred_time`, with untimed tasks last.|

 |Filtering                |      Scheduler.filter_tasks()       |       Filters by pet name and/or completion status.           |

 |Conflict detection       |     Scheduler.detect_conflicts()    |    Returns a warning when pending tasks share the same time   |

 |Recurring tasks          |         Task.mark_complete()        |       Creates the next daily or weekly task when one is completed. |
## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
