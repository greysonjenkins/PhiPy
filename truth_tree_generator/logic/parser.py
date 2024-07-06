from enum import Enum

class TokenType(Enum):
    ATOM = 1
    AND = 2
    OR = 3
    NOT = 4
    IMPLIES = 5
    IFF = 6
    LPAREN = 7
    RPAREN = 8

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class ASTNode:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

def tokenize(sentence):
    tokens = []
    i = 0
    while i < len(sentence):
        if sentence[i].isspace():
            i += 1
            continue
        elif sentence[i].isalpha():
            tokens.append(Token(TokenType.ATOM, sentence[i]))
        elif sentence[i] == '∧':
            tokens.append(Token(TokenType.AND, '∧'))
        elif sentence[i] == '∨':
            tokens.append(Token(TokenType.OR, '∨'))
        elif sentence[i] == '¬':
            tokens.append(Token(TokenType.NOT, '¬'))
        elif sentence[i] == '→':
            tokens.append(Token(TokenType.IMPLIES, '→'))
        elif sentence[i:i+2] == '↔':
            tokens.append(Token(TokenType.IFF, '↔'))
            i += 1
        elif sentence[i] == '(':
            tokens.append(Token(TokenType.LPAREN, '('))
        elif sentence[i] == ')':
            tokens.append(Token(TokenType.RPAREN, ')'))
        else:
            raise ValueError(f"Unexpected character: {sentence[i]}")
        i += 1
    return tokens

def parse_sentences(sentences):
    parsed_sentences = []
    for sentence in sentences:
        tokens = tokenize(sentence)
        ast = parse_sentence(tokens)
        parsed_sentences.append(ast)
    return parsed_sentences

def parse_sentence(tokens):
    def parse_iff():
        left = parse_implies()
        while tokens and tokens[0].type == TokenType.IFF:
            tokens.pop(0)
            right = parse_implies()
            left = ASTNode(TokenType.IFF, left=left, right=right)
        return left

    def parse_implies():
        left = parse_or()
        while tokens and tokens[0].type == TokenType.IMPLIES:
            tokens.pop(0)
            right = parse_or()
            left = ASTNode(TokenType.IMPLIES, left=left, right=right)
        return left

    def parse_or():
        left = parse_and()
        while tokens and tokens[0].type == TokenType.OR:
            tokens.pop(0)
            right = parse_and()
            left = ASTNode(TokenType.OR, left=left, right=right)
        return left

    def parse_and():
        left = parse_not()
        while tokens and tokens[0].type == TokenType.AND:
            tokens.pop(0)
            right = parse_not()
            left = ASTNode(TokenType.AND, left=left, right=right)
        return left

    def parse_not():
        if tokens and tokens[0].type == TokenType.NOT:
            tokens.pop(0)
            return ASTNode(TokenType.NOT, left=parse_not())
        return parse_atom()

    def parse_atom():
        if not tokens:
            raise ValueError("Unexpected end of input")
        if tokens[0].type == TokenType.LPAREN:
            tokens.pop(0)
            result = parse_iff()
            if not tokens or tokens.pop(0).type != TokenType.RPAREN:
                raise ValueError("Mismatched parentheses")
            return result
        elif tokens[0].type == TokenType.ATOM:
            return ASTNode(TokenType.ATOM, value=tokens.pop(0).value)
        else:
            raise ValueError(f"Unexpected token: {tokens[0].value}")

    result = parse_iff()
    if tokens:
        raise ValueError(f"Unexpected tokens at end of input: {' '.join(t.value for t in tokens)}")
    return result

def ast_to_string(node):
    if node.type == TokenType.ATOM:
        return node.value
    elif node.type == TokenType.NOT:
        return f"¬({ast_to_string(node.left)})"
    elif node.type in [TokenType.AND, TokenType.OR, TokenType.IMPLIES, TokenType.IFF]:
        op = {TokenType.AND: '∧', TokenType.OR: '∨', TokenType.IMPLIES: '→', TokenType.IFF: '↔'}[node.type]
        return f"({ast_to_string(node.left)} {op} {ast_to_string(node.right)})"
    else:
        raise ValueError(f"Unknown node type: {node.type}")

# Example usage and testing
if __name__ == "__main__":
    test_sentences = [
        "P ∧ Q",
        "P ∨ Q",
        "P → Q",
        "P ↔ Q",
        "¬P",
        "¬(P ∧ Q)",
        "(P ∧ Q) ∨ R",
        "P → (Q ∨ R)",
        "¬P ∨ (Q ∧ R)",
        "(P → Q) ↔ (¬P ∨ Q)"
    ]

    for sentence in test_sentences:
        print(f"Original: {sentence}")
        try:
            parsed = parse_sentences([sentence])[0]
            print(f"Parsed:   {ast_to_string(parsed)}")
        except ValueError as e:
            print(f"Error:    {str(e)}")
        print()