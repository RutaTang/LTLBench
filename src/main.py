from src.core.query import generate_ltl_formulas

if __name__ == '__main__':
    f_length = 3
    n = 1
    formulas = generate_ltl_formulas(f_length, n)
    for formula in formulas:
        print(formula)
