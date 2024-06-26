import re
import nltk

class Predicate_Logic_Parser:
    def __init__(self) -> None:
        self.operators = ['⊕', '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ',']
        self.symbol_regex = re.compile(r'[^⊕∨∧→↔∀∃¬(),]+')

        self.cfg_template = """
        S -> F | Q F | '¬' S | '(' S ')'
        Q -> QUANT VAR | QUANT VAR Q
        F -> '¬' '(' F ')' | '(' F ')' | F OP F | L
        OP -> '⊕' | '∨' | '∧' | '→' | '↔'
        L -> '¬' PRED '(' TERMS ')' | PRED '(' TERMS ')'
        TERMS -> TERM | TERM ',' TERMS
        TERM -> CONST | VAR
        QUANT -> '∀' | '∃'
        """

    def text_to_tree(self, rules):
        rules = self.reorder_quantifiers(rules)

        r, parsed_string = self.split(rules)
        cfg_string = self.make_cfg_str(r)

        grammar = nltk.CFG.fromstring(cfg_string)
        parser = nltk.ChartParser(grammar)
        tree = parser.parse_one(r)

        return tree

    def reorder_quantifiers(self, rules):
        matches = re.findall(r'[∃∀]\w', rules)
        for match in matches[::-1]:
            rules = '%s ' % match + rules.replace(match, '', 1)
        return rules

    def split(self, s):
        for operator in self.operators:
            s = s.replace(operator, ' %s ' % operator)
        r = [e.strip() for e in s.split()]
        # Remove ' from string if it contains any: causes an error in cfg parsing
        r = [e.replace('\'', '') for e in r]
        r = [e for e in r if e != '']

        # Get rid of spaces (e.g., convert "Predicate Logic Parser" to "PredicateLogicParser")
        result = []
        current_string_list = []
        for e in r:
            if (len(e) > 1) and self.symbol_regex.match(e):
                current_string_list.append(e[0].upper() + e[1:])
            else:
                if len(current_string_list) > 0:
                    result.extend([''.join(current_string_list), e])
                else:
                    result.extend([e])
                current_string_list = []
        if len(current_string_list) > 0:
            result.append(''.join(current_string_list))

        # Re-generate the string
        string_list = []
        for index, e in enumerate(r):
            if re.match(r'[⊕∨∧→↔]', e):
                string_list.append(' %s ' % e)
            elif re.match(r',', e):
                string_list.append('%s ' % e)
            elif (len(e) == 1) and re.match(r'\w', e):
                if ((index - 1) >= 0) and ((r[index - 1] == '∃') or (r[index - 1] == '∀')):
                    string_list.append('%s ' % e)
                else:
                    string_list.append(e)
            else:
                string_list.append(e)

        return result, ''.join(string_list)

    def make_cfg_str(self, token_list):
        symbol_list = list(set([e for e in token_list if self.symbol_regex.match(e)]))
        symbol_string = ' | '.join(["'%s'" % s for s in symbol_list])
        cfg_string = self.cfg_template + 'VAR -> %s\nPRED -> %s\nCONST -> %s' % (
            symbol_string, symbol_string, symbol_string)
        return cfg_string

    def find_variables(self, variable, tree):
        if isinstance(tree, str):
            return

        if tree.label() == 'VAR':
            variable.add(tree[0])
            return

        for child in tree:
            self.find_variables(variable, child)

    def resolve_symbols(self, tree):
        literals, constants, predicates = set(), set(), set()
        self.find_variables(literals, tree)
        self.resolve_preorder(tree, literals, constants, predicates)
        return literals, constants, predicates

    def resolve_preorder(self, tree, literals, constants, predicates):
        # Terminal nodes?
        if isinstance(tree, str):
            return

        if tree.label() == 'PRED':
            predicates.add(tree[0])
            return

        if tree.label() == 'TERM':
            sym = tree[0][0]
            if sym in literals:
                tree[0].set_label('VAR')
            else:
                tree[0].set_label('CONST')
                constants.add(sym)
            return

        for child in tree:
            self.resolve_preorder(child, literals, constants, predicates)

if __name__ == '__main__':
    print("Here are some examples of well-formed formulas (WFFs):\n"
          "∀x(Human(x) ∧ Athletic(x) ∧ Tall(x) → BasketballPlayer(x))\n"
          "∀x(Athlete(x) ∧ WinsGold(x, olympics) → OlympicChampion(x))\n"
          "¬∀x∃x(Movie(x) → HappyEnding(x))\n"
          "¬Divides(x,y) ∧ Divides(x,y)")
    argument = str(input("Enter a WFF:\n"))

    parser = Predicate_Logic_Parser()

    tree = parser.text_to_tree(argument)
    print(tree)
    tree.pretty_print()

    literals, constants, predicates = parser.resolve_symbols(tree)
    print('Literals: ', literals)
    print('Constants: ', constants)
    print('Predicates: ', predicates)
