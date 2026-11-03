from typing import Self


class Ordered:
    def __init__(self, value: int, tag: str = "") -> None:
        self.value = value
        self.tag = tag

    def __lt__(self, other: Self, /) -> bool:
        return self.value < other.value

    def __eq__(self, other: object, /) -> bool:
        raise AssertionError("Only strict comparison is part of the contract")


class TaggedInt(int):
    def __new__(cls, value: int, tag: str) -> Self:
        result = super().__new__(cls, value)
        result.tag = tag
        return result
