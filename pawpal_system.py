from dataclasses import dataclass, field

VALID_PRIORITIES = ("low", "medium", "high")
PRIORITY_ORDER = {'high': 0, 'medium': 1, 'low': 2}
VALID_FREQUENCIES = ('once', 'daily', 'weekly')


@dataclass
class Owner:
	name: str
	preferences: dict[str, object]
	pets: list["Pet"] = field(default_factory=list)

	def add_pet(self, pet: "Pet") -> None:
		pet.owner = self
		self.pets.append(pet)

	def remove_pet(self, pet: "Pet") -> None:
		self.pets.remove(pet)

	def get_all_tasks(self) -> list["Task"]:
		return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Pet:
	name: str
	species: str
	owner: Owner = field(repr=False, compare=False)
	tasks: list["Task"] = field(default_factory=list)

	def add_task(self, task: "Task") -> None:
		task.pet = self
		self.tasks.append(task)

	def remove_task(self, task: "Task") -> None:
		self.tasks.remove(task)


@dataclass
class Task:
	title: str
	duration_minutes: int
	priority: str
	pet: Pet = field(repr=False, compare=False)
	frequency: str = 'daily'
	completed: bool = False

	def __post_init__(self) -> None:
		if self.duration_minutes <= 0:
			raise ValueError("duration_minutes must be greater than 0")
		if self.priority not in VALID_PRIORITIES:
			raise ValueError(f"priority must be one of {VALID_PRIORITIES}")
		if self.frequency not in VALID_FREQUENCIES:
			raise ValueError(f"frequency must be one of {VALID_FREQUENCIES}")

	def mark_complete(self) -> None:
		self.completed = True


@dataclass
class ScheduledTask:
	task: Task
	start_time: str


class Scheduler:
	def __init__(self, owner: Owner, available_minutes: int) -> None:
		if available_minutes <= 0:
			raise ValueError("available_minutes must be greater than 0")
		self.owner = owner
		self.available_minutes = available_minutes
		self.plan: list[ScheduledTask] = []
		self.skipped: list[Task] = []

	def get_all_tasks(self) -> list[Task]:
		return self.owner.get_all_tasks()

	def get_pending_tasks(self) -> list[Task]:
		return [task for task in self.get_all_tasks() if task.completed is False]

	def sort_tasks(self, tasks: list[Task]) -> list[Task]:
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
