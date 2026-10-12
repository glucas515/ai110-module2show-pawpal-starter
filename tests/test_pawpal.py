from pawpal_system import Owner, Pet, Task


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