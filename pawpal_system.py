from dataclasses import dataclass


@dataclass
class Owner:
	name: str
	preferences: dict[str, object]


@dataclass
class Pet:
	name: str
	species: str
	owner: Owner


@dataclass
class Task:
	title: str
	duration_minutes: int
	priority: str
	pet: Pet


class Scheduler:
	def __init__(self, tasks: list[Task], available_minutes: int) -> None:
		self.tasks = tasks
		self.available_minutes = available_minutes

	def generate_plan(self) -> None:
		"""Create a schedule from the tasks and available time."""
		pass

	def explain_plan(self) -> None:
		"""Describe why the scheduled tasks were selected and ordered."""
		pass
