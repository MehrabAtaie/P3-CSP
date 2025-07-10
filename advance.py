import copy

class SmartEquationCSP:
    def __init__(self, chars):
        self.chars = chars
        self.n = len(chars)
        self.result = None
        self.counter = {}
        for ch in chars:
            self.counter[ch] = self.counter.get(ch, 0) + 1


    def is_valid_equation(self, eq_str):
        if eq_str.count('=') != 1:
            return False
        left, right = eq_str.split('=')
        if not left or not right:
            return False
        operators = set('+-*/')
        if eq_str[0] in operators or eq_str[-1] in operators or eq_str[0] == '=' or eq_str[-1] == '=':
            return False
        for i in range(1, len(eq_str)):
            if (eq_str[i] in operators and eq_str[i-1] in operators) or (eq_str[i] == '=' and eq_str[i-1] == '='):
                return False
        try:
            left_val = eval(left)
            right_val = eval(right)
            return left_val == right_val
        except:
            return False

    def is_partial_valid(self, assignment):
        eq_str = ''.join([a for a in assignment if a is not None])
        operators = '+-*/'
        if not eq_str:
            return True

        # بیش از یک مساوی مجاز نیست
        if eq_str.count('=') > 1:
            return False

        # نباید با عملگر یا مساوی شروع شود
        if eq_str[0] in operators + '=':
            return False

        # دو عملگر یا دو مساوی یا عملگر و مساوی نباید کنار هم باشند
        for i in range(1, len(eq_str)):
            if (eq_str[i] in operators + '=' and eq_str[i-1] in operators + '='):
                return False

        # اگر مساوی وجود دارد، نباید هر دو سمتش خالی باشد (اما مجاز است فقط یک سمت ناقص باشد)
        if '=' in eq_str:
            left, right = eq_str.split('=', 1)
            if not left:
                return False
            # فقط اگر بعد مساوی شروع شد (یعنی سمت راست مساوی خالی باشد)، مسیر قطع شود.
            # سمت راست می‌تواند ناقص باشد تا بعداً کامل شود.

        return True

    def mrv(self, assignment, available):
        for i in range(self.n):
            if assignment[i] is None:
                return i
        return None

    def lcv(self, var, assignment, available):
        value_options = [ch for ch in available if available[ch] > 0]
        return sorted(value_options, key=lambda ch: -available[ch])

    def ac2(self, assignment, available):
        for i in range(self.n):
            if assignment[i] is not None:
                continue
            if all(available[ch] == 0 for ch in available):
                return False
        return True

    def forward_checking(self, available, value):
        if available[value] > 0:
            available[value] -= 1
            return True
        return False

    def backtrack(self, assignment, available, depth=0):
        if self.result:
            return
        if None not in assignment:
            eq_str = ''.join(assignment)
            if self.is_valid_equation(eq_str):
                self.result = eq_str
            return

        var = self.mrv(assignment, available)
        if var is None:
            return
        values = self.lcv(var, assignment, available)
        for value in values:
            assignment_new = assignment[:]
            available_new = available.copy()
            assignment_new[var] = value

            # Forward checking
            if not self.forward_checking(available_new, value):
                continue

            # Prune نحوی
            if not self.is_partial_valid(assignment_new):
                continue

            # AC2
            if not self.ac2(assignment_new, available_new):
                continue

            self.backtrack(assignment_new, available_new, depth+1)
            if self.result:
                break

    def solve(self):
        self.result = None
        assignment = [None] * self.n
        available = self.counter.copy()
        if not self.ac2(assignment, available):
            return None
        self.backtrack(assignment, available)
        return self.result
