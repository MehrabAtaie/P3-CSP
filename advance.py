import copy

class SmartEquationCSP:
    def __init__(self, chars):
        self.chars = chars
        self.n = len(chars)
        # دامنه اولیه: هر متغیر می‌تونه هر کاراکتری بگیره (ابتدا)
        self.init_domains = [set(chars) for _ in range(self.n)]
        self.result = None

    def is_valid_equation(self, eq_str):
        if eq_str.count('=') != 1:
            return False
        left, right = eq_str.split('=')
        if not left or not right:
            return False
        operators = set('+-*/')
        if eq_str[0] in operators or eq_str[-1] in operators:
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

    def mrv(self, assignment, domains):
        """انتخاب متغیری که کمترین دامنه ممکن دارد و مقدار نگرفته"""
        unassigned = [i for i in range(self.n) if assignment[i] is None]
        # کوچکترین دامنه
        min_domain = min([len(domains[i]) for i in unassigned])
        candidates = [i for i in unassigned if len(domains[i]) == min_domain]
        return candidates[0]  # فقط اولی را انتخاب می‌کنیم
