import signal
import sys

from predicate_logic_parser import PredicateLogicParser


class PredicateFormula:
    def __init__(self, formula) -> None:
        self.parser = PredicateLogicParser()

        def handler(signum, f):
            raise Exception("Error: Timed out")

        # Set handler and 60-second limit
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(60)
        try:
            tree = self.parser.text_to_tree(formula)
        except Exception as ex:
            tree = None
            self.is_wff = False
            return

        self.tree = tree
        if tree is None:
            self.is_wff = False
        else:
            self.is_wff = True
            self.variables, self.constants, self.predicates = self.parser.resolve_symbols(tree)

    def __str__(self) -> str:
        _, rules = self.parser.split(''.join(self.tree.leaves()))
        return rules

    def is_wff(self):
        return self.is_wff

    def _get_formula_template(self, tree, mappings):
        for i, subtree in enumerate(tree):
            if isinstance(subtree, str):
                if subtree in mappings:
                    new_label = mappings[subtree]
                    tree[i] = new_label
            else:
                self._get_formula_template(subtree, mappings)

    def get_formula_template(self):
        template = self.tree.copy(deep=True)
        mappings = {}
        for i, f in enumerate(self.predicates):
            mappings[f] = 'P%d' % i
        for i, f in enumerate(self.constants):
            mappings[f] = 'C%d' % i

        self._get_formula_template(template, mappings)
        self.template = template
        _, self.template_string = self.parser.split(''.join(self.template.leaves()))
        return mappings, self.template_string

if __name__ == '__main__':
    print("Here are some examples of well-formed formulas (WFFs):\n"
          "∀x(Human(x) ∧ Athletic(x) ∧ Tall(x) → BasketballPlayer(x))\n"
          "∀x(Athlete(x) ∧ WinsGold(x, olympics) → OlympicChampion(x))\n"
          "∃x∃y(Czech(x) ∧ Book(y) ∧ Author(x, y) ∧ Publish(y, 1946))\n"
          "¬∀x∃x(Movie(x) → HappyEnding(x))\n"
          "¬Divides(x,y) ∧ Divides(x,y)")

    while True:
        user_input = str(input("\nEnter a WFF (or enter 'q' to exit):\n"))

        if user_input == 'q':
            sys.exit("Quitting program...")
        else:
            predicate_rule = PredicateFormula(user_input)
            if predicate_rule.is_wff:
                print("Rule:", predicate_rule)
                print("Variables:", predicate_rule.variables)
                print("Constants:", predicate_rule.constants)
                print("Predicates:", predicate_rule.predicates)
                mappings, template = predicate_rule.get_formula_template()
                print("Template:", template)
                print("Mappings:", mappings)
            else:
                print("Error: Not a well-formed formula.")