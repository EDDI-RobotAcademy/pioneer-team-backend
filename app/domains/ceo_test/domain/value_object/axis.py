from enum import Enum


class JudgingAxis(str, Enum):
    Ti = "Ti"
    Te = "Te"
    BALANCED = "Balanced"


class EmpathyAxis(str, Enum):
    Fi = "Fi"
    Fe = "Fe"
    BALANCED = "Balanced"
