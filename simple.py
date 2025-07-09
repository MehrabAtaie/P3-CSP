class SimpleEquationCSP:
    def __init__(self, chars):
        self.chars = chars
        self.n = len(chars)
        self.used = [False] * self.n
        self.result = None

    def is_valid_equation(self, eq_str):
        # فقط یک مساوی باید باشد
        if eq_str.count('=') != 1:
            return False
        left, right = eq_str.split('=')
        # هیچکدام نباید خالی باشد
        if not left or not right:
            return False
        operators = set('+-*/')
        # شروع/پایان با عملگر نباشد
        if eq_str[0] in operators or eq_str[-1] in operators:
            return False
        # دو عملگر یا دو مساوی پشت هم نباشد
        for i in range(1, len(eq_str)):
            if (eq_str[i] in operators and eq_str[i-1] in operators) or (eq_str[i] == '=' and eq_str[i-1] == '='):
                return False
        try:
            # سمت چپ و راست مساوی باید مقدار مساوی بدهند
            left_val = eval(left)
            right_val = eval(right)
            return left_val == right_val
        except:
            return False

    def backtrack(self, path):
        if self.result:  # اگر قبلاً جواب پیدا شده، ادامه نده
            return
        if len(path) == self.n:
            eq_str = ''.join(path)
            if self.is_valid_equation(eq_str):
                self.result = eq_str
            return
        for i in range(self.n):
            if not self.used[i]:
                self.used[i] = True
                path.append(self.chars[i])
                self.backtrack(path)
                path.pop()
                self.used[i] = False

    def solve(self):
        self.result = None
        self.backtrack([])
        return self.result

