import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner and Pets")
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", preferences={"day_start": "08:00"})
owner = st.session_state.owner

owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    pet = Pet(pet_name, species, owner)
    owner.add_pet(pet)
    st.success(f"Added {pet_name}.")

if owner.pets:
    st.table([{"name": pet.name, "species": pet.species} for pet in owner.pets])
else:
    st.info("No pets yet.")

available_minutes = st.number_input('Available minutes today', min_value=1, max_value=720, value=60)
scheduler = Scheduler(owner, available_minutes)

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if not owner.pets:
    st.info("Add a pet first.")
else:
    pet_index = st.selectbox('Pet', range(len(owner.pets)), format_func=lambda i: owner.pets[i].name)
    selected_pet = owner.pets[pet_index]
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        preferred_time = st.text_input("Preferred time (HH:MM, optional)", value="")
    with col5:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], index=1)

    if st.button("Add task"):
        try:
            stripped_time = preferred_time.strip()
            task = Task(
                task_title,
                int(duration),
                priority,
                selected_pet,
                frequency=frequency,
                preferred_time=stripped_time or None,
            )
            selected_pet.add_task(task)
            st.success(f"Added {task_title} for {selected_pet.name}.")
        except ValueError as error:
            st.error(str(error))

filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    selected_pet_name = st.selectbox("Filter by pet", ["All pets"] + [pet.name for pet in owner.pets])
with filter_col2:
    selected_status = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

pet_filter = None if selected_pet_name == "All pets" else selected_pet_name
completed_filter = {"All": None, "Pending": False, "Completed": True}[selected_status]
tasks = scheduler.sort_by_time(
    scheduler.filter_tasks(pet_name=pet_filter, completed=completed_filter)
)
if tasks:
    st.table([
        {
            "pet": task.pet.name,
            "title": task.title,
            "time": task.preferred_time if task.preferred_time is not None else "no time",
            "duration_minutes": task.duration_minutes,
            "priority": task.priority,
            "frequency": task.frequency,
            "status": "done" if task.completed else "pending",
        }
        for task in tasks
    ])
else:
    st.info("No tasks match.")

st.divider()

st.subheader("Build Schedule")
st.caption("Build today's plan from the pending tasks.")

if st.button("Generate schedule"):
    scheduler.generate_plan()
    if not scheduler.plan:
        st.info("No tasks to schedule yet. Add a task above.")
    else:
        total_minutes = sum(item.task.duration_minutes for item in scheduler.plan)
        st.success(
            f"Scheduled {len(scheduler.plan)} tasks, using {total_minutes} of "
            f"{scheduler.available_minutes} available minutes."
        )
        st.table([
            {
                "start": item.start_time,
                "task": item.task.title,
                "pet": item.task.pet.name,
                "priority": item.task.priority,
                "duration_minutes": item.task.duration_minutes,
            }
            for item in scheduler.plan
        ])

    if scheduler.skipped:
        skipped_tasks = ", ".join(
            f"{task.title} ({task.pet.name})" for task in scheduler.skipped
        )
        st.warning(
            f"Skipped tasks: {skipped_tasks}. Increase the available minutes to schedule them."
        )

    for conflict in scheduler.detect_conflicts():
        st.warning(f"{conflict} Change one of those tasks' times to resolve the conflict.")

    with st.expander("Why this plan?"):
        st.text(scheduler.explain_plan())
