# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design has four classes: Owner, Pet, Task, and Scheduler.

- Owner holds a name and a dictionary of preferences (e.g., preferred start time, max daily care minutes). It's a simple data holder with no behavior of its own.
- Pet holds a name, species, and a reference back to its Owner. Also just a data holder.
- Task represents a single care task: a title, duration in minutes, priority (low/medium/high), and a reference to the Pet it belongs to. Another data holder.
- Scheduler is the only class with real behavior. It takes a list of Tasks and the available time for the day, and is responsible for generate_plan() (choosing and ordering tasks that fit the time budget, prioritizing higher-priority tasks) and explain_plan() (describing why each task was included/excluded and in what order).

I kept Owner, Pet, and Task as plain data holders (implemented as Python dataclasses) and put all the actual logic in one place (Scheduler), so the scheduling behavior isn't scattered across multiple classes.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, my design changed after I had Copilot review my class skeleton. It flagged four findings and one implementation risk, and I made code changes for most of them.

- ScheduledTask: My original Task only described what needed to be done, but a schedule also has to say when. I added a ScheduledTask class (a task plus a start_time) and gave Scheduler a plan list to hold the results.
- Explanation output: explain_plan() originally returned nothing, so the UI would have had nothing to display. It now returns a string describing each scheduled task, or "No tasks scheduled." if the plan is empty.
- Scheduler and Owner: Scheduler originally took both an owner and a separate list of tasks, which created two sources of truth. I removed the tasks parameter and added get_all_tasks(), which collects tasks from the owner's pets.
- Owner, Pet, and Task relationships: The code only had back-references (Pet.owner, Task.pet), so there was no way to go from an owner to their tasks. I added Owner.pets and Pet.tasks using field(default_factory=list) so instances don't share one mutable list. I also set the back-references to repr=False and compare=False so printing or comparing objects can't recurse forever.
- Validation: Following Copilot's implementation-risk note, I added a VALID_PRIORITIES constant. Task now raises a ValueError for non-positive durations or unknown priorities, and Scheduler raises one for non-positive available_minutes.
- Time constraints (partially addressed): ScheduledTask has a start_time, but the scheduler still doesn't accept real time constraints like a day-start time or deadlines. I deliberately deferred this to keep the first version simple and explainable (see Section 2).

As a result, Owner and Pet are no longer pure data holders like I described in 1a. They now manage their own relationships, while Scheduler still holds all of the scheduling logic.

**c. Core user actions**

A user of PawPal+ should be able to:
1. Add a pet care task (Title, duration, priority)
2. Enter basic owner and pet info (name,species, preferences)
3. Generate a daily schedule that picks and orders based on time and priority, with explaination of why

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler considers the minutes available in the day, each task's priority (high, medium, low), how long each task takes, and whether a task is still pending and due today. It also reads an optional day_start preference from the owner, which defaults to 08:00. Time and priority matter most, because a plan that doesn't fit the day, or that puts grooming ahead of feeding, isn't useful. Tasks are ordered by priority, then shortest first, and packed back to back from the day start. Anything that doesn't fit is skipped and listed. A task's preferred_time is used for sorting and conflict warnings, but the plan doesn't place tasks at those times

**b. Tradeoffs**


My conflict detection only checks for exact time matches. It warns when two pending tasks have the same preferred_time, but it doesn't check whether one task's duration runs into another's start. For example, a 30-minute walk at 08:00 and a task at 08:15 would not be flagged. I chose this because it is simple, fast, and easy to explain to a pet owner, and because generate_plan() places tasks back to back, so the plan itself can never contain overlaps. The cost is that two tasks with different preferred times can still clash in real life. With more time I would compare each task's start and end time (start plus duration) to catch overlaps.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used GitHub Copilot in VS Code, mostly in Agent mode, to write and edit code, and a separate AI chat to plan each step and double-check Copilot's diffs before I clicked Keep. Copilot was most effective on multi-step edits where it could read the files, change them, and run a quick check (py_compile or pytest) before I approved. The most helpful prompts were narrow and explicit, such as "change only the Scheduler class," "don't modify pawpal_system.py," and "keep existing methods exactly as they are." Asking for a plan in Ask mode before building, for the test plan and the UML updates, also saved time.

Using a new chat for each feature kept Copilot focused on one change and kept each diff small enough to review properly. It also stopped old instructions from leaking into new tasks. Planning chats (test plan, UML, algorithm ideas) stayed separate from implementation chats, so ideas didn't get mixed into the code.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When I asked for a lightweight conflict check that never crashes, Copilot wrapped the whole method in try/except Exception and returned an empty list on any error. I removed it, because a real bug would have shown up as "no conflicts" and not as an error. The method already returns a warning string when there is a conflict, which is all the feature needed. I also kept recurring tasks simpler than Copilot's planning suggestion, which generated occurrences per day and tracked completion on each one. In my version, marking a daily or weekly task complete creates one new task due tomorrow or in seven days.

I read every diff before clicking Keep and ran pytest and main.py after each change. Reading diffs caught a change that left the old tasks parameter in the Scheduler signature. Running the Streamlit app caught a bug the diff didn't show: a task displayed a success message but never appeared in the table, because the pet dropdown returned a different Pet object than the one stored in owner.pets. I fixed it by selecting the pet by its position in the list.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I wrote seven pytest tests. They check that marking a task complete changes its status and that adding a task increases a pet's task count. They check that sort_by_time returns tasks in clock order with untimed tasks last. They check that completing a daily task creates one new task due tomorrow without duplicating it if called twice, and that a one-time task doesn't recur. They also check that detect_conflicts flags two pending tasks at the same time and stays quiet for different times or a completed task. These are the behaviors the demo and the UI depend on, so a regression would show up right away.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

About 4 out of 5. The sorting, recurrence and conflict logic are covered by tests, and I checked the full plan through main.py and the Streamlit app. I'm not at 5 because generate_plan() has no unit tests yet. Next I would test a task that exactly fills the remaining time, a skipped task followed by a shorter one that still fits, an empty schedule, filtering with duplicate pet names, input validation errors, and conflicts between overlapping times and not just identical ones.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with building in layers. The classes and scheduling logic worked in a CLI demo and in tests before I touched Streamlit, so when the UI misbehaved I knew where to look. Keeping responsibilities clear also helped: the Scheduler gets its tasks through the Owner instead of keeping its own copy, which made later features easy to add.


**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would let generate_plan() place tasks at their preferred times instead of only using them for sorting and conflict warnings, and detect overlapping durations and not just identical start times. I would add a way to mark a task complete from the Streamlit app, since recurrence is currently only demonstrated in main.py and the tests. I would also add unit tests for generate_plan() and save the data so it survives restarting the app.


**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Working as the lead architect meant I made the design decisions and the AI did most of the typing. Copilot did what the prompt said, including things I didn't want, like swallowing errors, and sometimes only part of what I asked for. What worked best was small, specific prompts, reading every diff, and checking behavior with tests and by running the app. Decisions about what each class owns, what to leave out, and what counts as a conflict were mine to make, and the AI couldn't make them for me.
