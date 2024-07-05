from typing import List
from utils.logic import Atom, Not, And, Or, Implies, Formula


def tokenize(s: str) -> List[str]:
    return s.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(tokens: List[str]) -> Formula:
    if not tokens:
        raise ValueError("Unexpected EOF")

    token = tokens.pop(0)
    if token == '(':
        op = tokens.pop(0)
        if op == 'not':
            arg = parse(tokens)
            tokens.pop(0)  # Remove closing parenthesis
            return Not(arg)
        elif op in ['and', 'or', 'implies']:
            left = parse(tokens)
            right = parse(tokens)
            tokens.pop(0)  # Remove closing parenthesis
            if op == 'and':
                return And(left, right)
            elif op == 'or':
                return Or(left, right)
            else:
                return Implies(left, right)
        else:
            raise ValueError(f"Unknown operator: {op}")
    else:
        return Atom(token)


def parse_argument(s: str) -> Formula:
    tokens = tokenize(s)
    return parse(tokens)
