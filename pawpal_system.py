from dataclasses import dataclass, field
from datetime import date, timedelta

VALID_PRIORITIES = ("low", "medium", "high")
PRIORITY_ORDER = {'high': 0, 'medium': 1, 'low': 2}
VALID_FREQUENCIES = ('once', 'daily', 'weekly')


@dataclass
class Owner:
	name: str
	preferences: dict[str, object]
	pets: list["Pet"] = field(default_factory=list)

	def add_pet(self, pet: "Pet") -> None:
		"""Add a pet to this owner's list of pets."""
		pet.owner = self
		self.pets.append(pet)

	def remove_pet(self, pet: "Pet") -> None:
		"""Remove a pet from this owner's list of pets."""
		self.pets.remove(pet)

	def get_all_tasks(self) -> list["Task"]:
		"""Return every task assigned to the owner's pets."""
		return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Pet:
	name: str
	species: str
	owner: Owner = field(repr=False, compare=False)
	tasks: list["Task"] = field(default_factory=list)

	def add_task(self, task: "Task") -> None:
		"""Add a task to this pet's task list."""
		task.pet = self
		self.tasks.append(task)

	def remove_task(self, task: "Task") -> None:
		"""Remove a task from this pet's task list."""
		self.tasks.remove(task)


@dataclass
class Task:
	title: str
	duration_minutes: int
	priority: str
	pet: Pet = field(repr=False, compare=False)
	frequency: str = 'daily'
	completed: bool = False
	preferred_time: str | None = None
	due_date: date | None = None

	def __post_init__(self) -> None:
		"""Validate the task data during initialization."""
		if self.duration_minutes <= 0:
			raise ValueError("duration_minutes must be greater than 0")
		if self.priority not in VALID_PRIORITIES:
			raise ValueError(f"priority must be one of {VALID_PRIORITIES}")
		if self.frequency not in VALID_FREQUENCIES:
			raise ValueError(f"frequency must be one of {VALID_FREQUENCIES}")
		if self.preferred_time is not None:
			valid_shape = (
				len(self.preferred_time) == 5
				and self.preferred_time[2] == ':'
				and self.preferred_time[:2].isascii()
				and self.preferred_time[:2].isdigit()
				and self.preferred_time[3:].isascii()
				and self.preferred_time[3:].isdigit()
			)
			if not valid_shape:
				raise ValueError("preferred_time must be a valid 24-hour HH:MM string")
			hours, minutes = (int(part) for part in self.preferred_time.split(':'))
			if hours > 23 or minutes > 59:
				raise ValueError("preferred_time must be a valid 24-hour HH:MM string")

	def mark_complete(self) -> "Task | None":
		"""Complete this task and create its next recurrence when applicable."""
		if self.completed:
			return None
		self.completed = True
		if self.frequency == 'once':
			return None

		days_until_due = 1 if self.frequency == 'daily' else 7
		new_task = Task(
			self.title,
			self.duration_minutes,
			self.priority,
			self.pet,
			frequency=self.frequency,
			completed=False,
			preferred_time=self.preferred_time,
			due_date=date.today() + timedelta(days=days_until_due),
		)
		self.pet.add_task(new_task)
		return new_task


@dataclass
class ScheduledTask:
	task: Task
	start_time: str


class Scheduler:
	def __init__(self, owner: Owner, available_minutes: int) -> None:
		"""Initialize the scheduler with an owner and available minutes."""
		if available_minutes <= 0:
			raise ValueError("available_minutes must be greater than 0")
		self.owner = owner
		self.available_minutes = available_minutes
		self.plan: list[ScheduledTask] = []
		self.skipped: list[Task] = []

	def get_all_tasks(self) -> list[Task]:
		"""Return all tasks for the owner managed by this scheduler."""
		return self.owner.get_all_tasks()

	def sort_by_time(self, tasks: list[Task]) -> list[Task]:
		"""Sort tasks by preferred time, placing tasks without one last."""
		return sorted(tasks, key=lambda task: (task.preferred_time is None, task.preferred_time or ""))

	def filter_tasks(
		self,
		pet_name: str | None = None,
		completed: bool | None = None,
	) -> list[Task]:
		"""Return tasks matching the provided pet name and completion status."""
		tasks = self.get_all_tasks()
		if pet_name is not None:
			tasks = [task for task in tasks if task.pet.name == pet_name]
		if completed is not None:
			tasks = [task for task in tasks if task.completed == completed]
		return tasks

	def get_pending_tasks(self) -> list[Task]:
		"""Return the tasks that are still incomplete."""
		return [task for task in self.get_all_tasks() if task.completed is False]

	def sort_tasks(self, tasks: list[Task]) -> list[Task]:
		"""Sort tasks by priority and duration."""
		return sorted(
			tasks,
			key=lambda task: (PRIORITY_ORDER[task.priority], task.duration_minutes),
		)

	def generate_plan(self) -> None:
		"""Schedule ordered pending tasks within the available time and record skipped tasks."""
		self.plan.clear()
		self.skipped.clear()
		pending_tasks = self.sort_tasks(self.get_pending_tasks())
		day_start = self.owner.preferences.get('day_start', '08:00')
		hours, minutes = (int(part) for part in day_start.split(':'))
		current_minutes = hours * 60 + minutes
		minutes_used = 0

		for task in pending_tasks:
			if minutes_used + task.duration_minutes <= self.available_minutes:
				start_hours, start_minutes = divmod(current_minutes, 60)
				self.plan.append(
					ScheduledTask(task, f'{start_hours:02d}:{start_minutes:02d}')
				)
				current_minutes += task.duration_minutes
				minutes_used += task.duration_minutes
			else:
				self.skipped.append(task)

	def explain_plan(self) -> str:
		"""Return the explanation text for self.plan."""
		if not self.plan:
			return "No tasks scheduled."
		return "\n".join(
			f"{item.start_time} - {item.task.title} ({item.task.pet.name})"
			for item in self.plan
		)
