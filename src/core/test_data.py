from unittest import TestCase

from src.core.data import generate_problem


class Test(TestCase):
    def test_generate_problem(self):
        problem = generate_problem(number_of_events=3, formula_length=3)
        print(problem)
