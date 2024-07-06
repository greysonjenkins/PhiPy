# utils/parser.py
from typing import List
from utils.logic import Atom, Not, And, Or, Implies, Formula

def tokenize(s: str) -> List[str]:
    # Add space around parentheses and commas to tokenize properly
    s = s.replace('(', ' ( ').replace(')', ' ) ').replace(',', ' , ')
    return s.split()

def parse(tokens: List[str]) -> Formula:
    if not tokens:
        raise ValueError("Unexpected EOF")

    token = tokens.pop(0)
    if token == '(':
        raise ValueError("Unexpected '('")
    elif token in ['and', 'or', 'implies', 'not']:
        op = token
        tokens.pop(0)  # Remove opening parenthesis
        if op == 'not':
            arg = parse(tokens)
            tokens.pop(0)  # Remove closing parenthesis
            return Not(arg)
        else:
            left = parse(tokens)
            tokens.pop(0)  # Remove comma
            right = parse(tokens)
            tokens.pop(0)  # Remove closing parenthesis
            if op == 'and':
                return And(left, right)
            elif op == 'or':
                return Or(left, right)
            elif op == 'implies':
                return Implies(left, right)
    else:
        return Atom(token)

def parse_argument(s: str) -> Formula:
    tokens = tokenize(s)
    return parse(tokens)