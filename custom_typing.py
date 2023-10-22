from dataclasses import dataclass


@dataclass(frozen=True)
class OptimalParameters:
    height: list
    angle: list
    width: list


@dataclass(frozen=True)
class Boundary:
    left: float
    right: float
