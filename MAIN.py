from simple import SimpleEquationCSP
from advance import SmartEquationCSP

if __name__ == "__main__":
    inp = input()
    chars = eval(inp)

    simple_solver = SimpleEquationCSP(chars)
    print("جواب ساده:","\n", simple_solver.solve())
    
    advanced_solver = SmartEquationCSP(chars)
    print("جواب پیشرفته:", "\n", advanced_solver.solve())
