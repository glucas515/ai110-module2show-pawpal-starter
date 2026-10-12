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

**b. Tradeoffs**


My conflict detection only checks for exact time matches. It warns when two pending tasks have the same preferred_time, but it doesn't check whether one task's duration runs into another's start. For example, a 30-minute walk at 08:00 and a task at 08:15 would not be flagged. I chose this because it is simple, fast, and easy to explain to a pet owner, and because generate_plan() places tasks back to back, so the plan itself can never contain overlaps. The cost is that two tasks with different preferred times can still clash in real life. With more time I would compare each task's start and end time (start plus duration) to catch overlaps.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
