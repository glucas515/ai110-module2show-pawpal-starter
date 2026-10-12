from dataclasses import dataclass, field

VALID_PRIORITIES = ("low", "medium", "high")
VALID_FREQUENCIES = ('once', 'daily', 'weekly')


@dataclass
class Owner:
	name: str
	preferences: dict[str, object]
	pets: list["Pet"] = field(default_factory=list)


@dataclass
class Pet:
	name: str
	species: str
	owner: Owner = field(repr=False, compare=False)
	tasks: list["Task"] = field(default_factory=list)


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

	def get_all_tasks(self) -> list[Task]:
		return [task for pet in self.owner.pets for task in pet.tasks]

	def generate_plan(self) -> None:
		"""Populate self.plan using get_all_tasks() and self.owner.preferences."""
		pass

	def explain_plan(self) -> str:
		"""Return the explanation text for self.plan."""
		if not self.plan:
			return "No tasks scheduled."
		return "\n".join(
			f"{item.start_time} - {item.task.title} ({item.task.pet.name})"
			for item in self.plan
		)
