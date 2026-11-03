from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Job:
    finish: int
    start: int
    index: int
    weight: int


type State = int


type Step = tuple[State, int | None]


type Parents = list[Step]
