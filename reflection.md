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

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
