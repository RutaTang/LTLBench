from unittest import TestCase

import numpy as np

from src.generator.query import generate_ltl_formulas, convert_ltl_formula_to_nusmv, recursive_join, \
    convert_ltl_formula_to_nl, covert_ltl_formula_to_str_formula
from src.utils.types import ReferenceValue


class Test(TestCase):
    def test_generate_ltl_formulas(self):
        rng = np.random.default_rng(1)
        formulas = generate_ltl_formulas(
            rng=rng,
            states=["a", "b", "c"],
            formula_length=3,
            count_of_formulas=1,
        )
        # hard to test, just print it
        print(formulas)

    def test_convert_ltl_formula_to_nusmv(self):
        converted = convert_ltl_formula_to_nusmv(['F', ['G', ['!', "event2"]]])
        self.assertTrue(converted == "(F (G (! (state=event2))))")

    def test_recursive_join(self):
        s = recursive_join(['a', ['b', 'c']])
        self.assertTrue(s == "(a (b c))")

    def test_covert_ltl_formula_to_str(self):
        converted = covert_ltl_formula_to_str_formula(['F', ['G', ['!', "event2"]]])
        self.assertTrue(converted == "(F (G (! event2)))")

    def test_convert_ltl_formula_to_nl(self):
        h_idx = ReferenceValue(0)
        result = ReferenceValue('')
        last_case = convert_ltl_formula_to_nl(['!', ['b', '->', ['!', 'a']]], ['a', 'b'], h_idx, result)
        self.assertTrue(last_case == "C3")
        result = result.get()
        result = result.split('\n')
        result.remove('')
        self.assertTrue(len(result) == 3)
