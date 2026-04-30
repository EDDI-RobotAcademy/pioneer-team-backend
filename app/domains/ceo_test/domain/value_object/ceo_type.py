from dataclasses import dataclass


@dataclass(frozen=True)
class CEOType:
    code: str
    name: str
    description: str
