from dataclasses import dataclass


@dataclass(frozen=True)
class Score:
    ti: int
    te: int
    fi: int
    fe: int
