from dataclasses import dataclass


@dataclass
class Entry[T]:
    value: T
    extreme: T
