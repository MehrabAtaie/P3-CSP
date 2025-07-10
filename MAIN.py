from simple import SimpleEquationCSP
from advance import SmartEquationCSP

if __name__ == "__main__":
    inp = input()
    chars = eval(inp)
    
    advanced_solver = SmartEquationCSP(chars)
    print("جواب پیشرفته:")
    print(advanced_solver.solve())

    simple_solver = SimpleEquationCSP(chars)
    print("جواب ساده:")
    print(simple_solver.solve())