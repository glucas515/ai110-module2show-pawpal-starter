from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def build_scheduler():
	owner = Owner('Jordan', {})
	pet = Pet('Mochi', 'dog', owner)
	owner.add_pet(pet)
	return owner, pet, Scheduler(owner, available_minutes=60)


def test_mark_complete_changes_status():
	owner = Owner('Jordan', {})
	pet = Pet('Mochi', 'dog', owner)
	task = Task('Walk', 20, 'high', pet)

	assert task.completed is False
	task.mark_complete()
	assert task.completed is True


def test_add_task_increases_pet_task_count():
	owner = Owner('Jordan', {})
	pet = Pet('Mochi', 'dog', owner)

	assert len(pet.tasks) == 0
	task = Task('Walk', 20, 'high', pet)
	pet.add_task(task)
	assert len(pet.tasks) == 1


def test_sort_by_time_orders_chronologically():
	owner, pet, scheduler = build_scheduler()
	for title, preferred_time in (
		('Afternoon walk', '16:00'),
		('Morning meal', '08:00'),
		('Midday play', '12:30'),
		('Flexible grooming', None),
	):
		pet.add_task(Task(title, 15, 'medium', pet, preferred_time=preferred_time))

	sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())

	assert [task.preferred_time for task in sorted_tasks] == [
		'08:00', '12:30', '16:00', None
	]


def test_daily_task_recurs_next_day():
	_, pet, _ = build_scheduler()
	task = Task('Walk', 20, 'high', pet, frequency='daily')
	pet.add_task(task)

	next_task = task.mark_complete()

	assert task.completed is True
	assert len(pet.tasks) == 2
	assert next_task is not None
	assert next_task.completed is False
	assert next_task.due_date == date.today() + timedelta(days=1)
	task.mark_complete()
	assert len(pet.tasks) == 2


def test_once_task_does_not_recur():
	_, pet, _ = build_scheduler()
	task = Task('Bath', 30, 'low', pet, frequency='once')
	pet.add_task(task)

	assert task.mark_complete() is None
	assert len(pet.tasks) == 1


def test_detect_conflicts_flags_duplicate_times():
	_, pet, scheduler = build_scheduler()
	pet.add_task(Task('Walk', 20, 'high', pet, preferred_time='08:00'))
	pet.add_task(Task('Breakfast', 15, 'medium', pet, preferred_time='08:00'))

	warnings = scheduler.detect_conflicts()

	assert len(warnings) == 1
	assert '08:00' in warnings[0]


def test_no_conflict_for_distinct_or_completed_times():
	_, pet, scheduler = build_scheduler()
	first_task = Task('Walk', 20, 'high', pet, preferred_time='08:00')
	second_task = Task('Breakfast', 15, 'medium', pet, preferred_time='09:00')
	pet.add_task(first_task)
	pet.add_task(second_task)
	assert scheduler.detect_conflicts() == []

	second_task.preferred_time = '08:00'
	second_task.completed = True
	assert scheduler.detect_conflicts() == []