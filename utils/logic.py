# utils/logic.py
from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class Atom:
    name: str

@dataclass(frozen=True)
class Not:
    formula: 'Formula'

@dataclass(frozen=True)
class And:
    left: 'Formula'
    right: 'Formula'

@dataclass(frozen=True)
class Or:
    left: 'Formula'
    right: 'Formula'

@dataclass(frozen=True)
class Implies:
    left: 'Formula'
    right: 'Formula'

Formula = Union[Atom, Not, And, Or, Implies]