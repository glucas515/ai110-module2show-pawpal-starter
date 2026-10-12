from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
	owner = Owner("Jordan", {"day_start": "08:00"})

	mochi = Pet("Mochi", "dog", owner)
	whiskers = Pet("Whiskers", "cat", owner)
	owner.add_pet(mochi)
	owner.add_pet(whiskers)

	mochi.add_task(Task("Morning walk", 30, "high", mochi))
	mochi.add_task(Task("Feeding", 10, "high", mochi))
	whiskers.add_task(Task("Litter box", 15, "medium", whiskers))
	whiskers.add_task(Task("Grooming", 45, "low", whiskers))

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


if __name__ == "__main__":
	main()