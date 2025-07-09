from simple import SimpleEquationCSP
from advance import SmartEquationCSP

if __name__ == "__main__":
    inp = input()
    chars = eval(inp)

    simple_solver = SimpleEquationCSP(chars)
    advanced_solver = SmartEquationCSP(chars)

    print(simple_solver.solve())
    print("جواب پیشرفته:", advanced_solver.solve())
