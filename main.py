from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
	owner = Owner("Jordan", {"day_start": "08:00"})

	mochi = Pet("Mochi", "dog", owner)
	whiskers = Pet("Whiskers", "cat", owner)
	owner.add_pet(mochi)
	owner.add_pet(whiskers)

	whiskers.add_task(Task("Grooming", 45, "low", whiskers, preferred_time="08:00"))
	mochi.add_task(Task("Morning walk", 30, "high", mochi, preferred_time="08:00"))
	feeding_task = Task("Feeding", 10, "high", mochi, preferred_time="07:30")
	mochi.add_task(feeding_task)
	whiskers.add_task(Task("Litter box", 15, "medium", whiskers))

	scheduler = Scheduler(owner, available_minutes=60)
	scheduler.generate_plan()

	print("Today's Schedule")
	for item in scheduler.plan:
		task = item.task
		print(
			f"{item.start_time} - {task.title} ({task.pet.name}) "
			f"[{task.priority}, {task.duration_minutes} min]"
		)

	print("Skipped (not enough time)")
	for task in scheduler.skipped:
		print(
			f"{task.title} ({task.pet.name}) "
			f"[{task.priority}, {task.duration_minutes} min]"
		)

	feeding_task.mark_complete()

	print("Tasks sorted by time")
	for task in scheduler.sort_by_time(owner.get_all_tasks()):
		preferred_time = task.preferred_time or "no time"
		print(f"{preferred_time} - {task.title} ({task.pet.name})")

	print("Tasks for Mochi")
	for task in scheduler.filter_tasks(pet_name="Mochi"):
		print(f"{task.title} ({task.pet.name})")

	print("Completed tasks")
	for task in scheduler.filter_tasks(completed=True):
		print(f"{task.title} ({task.pet.name})")

	print("Pending tasks")
	for task in scheduler.filter_tasks(completed=False):
		print(f"{task.title} ({task.pet.name})")

	print("Conflicts")
	conflicts = scheduler.detect_conflicts()
	if conflicts:
		for warning in conflicts:
			print(warning)
	else:
		print("No conflicts")


if __name__ == "__main__":
	main()