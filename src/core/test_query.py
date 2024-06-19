from unittest import TestCase

from src.core.query import generate_ltl_formulas, convert_ltl_formula_to_NuSMV, recursive_join, conver_ltl_formula_to_NL


class Test(TestCase):
    def test_generate_ltl_formulas(self):
        formulas = generate_ltl_formulas(
            states={"a", "b", "c"},
            formula_length=3,
            count_of_formulas=1,
        )
        print(formulas)

    def test_convert_ltl_formula_to_NuSMV(self):
        converted = convert_ltl_formula_to_NuSMV(['F', ['G', ['!', "event2"]]])
        print(converted)

    def test_recursive_join(self):
        s = recursive_join(['a', ['b', 'c']])
        print(s)

    def test_conver_ltl_formula_to_NL(self):
        converted = conver_ltl_formula_to_NL(['!', ['F', ['!', 'a']]], {'a'})
        print(converted)
        converted = conver_ltl_formula_to_NL(['!', ['b', '&', ['!', 'a']]], {'a', 'b'})
        print(converted)
