from typing import Literal, NamedTuple

type EditKind = Literal["match", "replace", "delete", "insert"]


class Edit(NamedTuple):
    kind: EditKind
    source: str | None
    target: str | None


type Parents = list[bytearray]
