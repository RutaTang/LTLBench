from unittest import TestCase

import numpy as np

from src.generator.data import generate_problem


class Test(TestCase):
    def test_generate_problem(self):
        rng = np.random.default_rng(1)
        problem = generate_problem(rng=rng, number_of_events=3, formula_length=3)
        # hard to test, just print it
        print(problem)
