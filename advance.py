import copy

class SmartEquationCSP:
    def __init__(self, chars):
        self.chars = chars
        self.n = len(chars)
        self.result = None
        # شمارش تعداد هر کاراکتر ورودی (برای مقدارهای تکراری)
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

    def mrv(self, assignment, available):
        """انتخاب متغیر با کمترین مقدار مجاز باقیمانده"""
        unassigned = [i for i in range(self.n) if assignment[i] is None]
        min_count = min([sum(1 for ch in available if available[ch] > 0) for i in unassigned])
        for i in unassigned:
            if sum(1 for ch in available if available[ch] > 0) == min_count:
                return i

    def lcv(self, var, assignment, available):
        """مرتب‌سازی مقدارهای مجاز به ترتیب کمترین محدودیت روی انتخاب‌های آینده"""
        value_options = [ch for ch in available if available[ch] > 0]
        scores = []
        for value in value_options:
            # این معیار ساده می‌گه هر مقداری که بیشتر در available باشه، محدودیت کمتری ایجاد می‌کنه
            score = available[value]
            scores.append((value, score))
        scores.sort(key=lambda x: -x[1])  # بیشترین باقیمانده جلوتر (LCV واقعی خیلی تو این مدل فرقی نداره)
        return [v for v, s in scores]

    def ac2(self, assignment, available):
        """AC-2: بررسی کند آیا هنوز برای هر متغیر حل‌نشده مقدار مجاز باقی مانده است یا نه"""
        for i in range(self.n):
            if assignment[i] is not None:
                continue
            # اگر هیچ مقداری برای این متغیر باقی نمونده، ناسازگار است
            if all(available[ch] == 0 for ch in available):
                return False
        return True

    def backtrack(self, assignment, available, depth=0):
        if self.result:
            return
        if None not in assignment:
            eq_str = ''.join(assignment)
            if self.is_valid_equation(eq_str):
                self.result = eq_str
            return

        var = self.mrv(assignment, available)
        values = self.lcv(var, assignment, available)

        for value in values:
            assignment_new = assignment[:]
            available_new = available.copy()
            assignment_new[var] = value
            available_new[value] -= 1

            # اجرای AC-2 بعد از هر مقداردهی
            if not self.ac2(assignment_new, available_new):
                continue

            self.backtrack(assignment_new, available_new, depth+1)
            if self.result:
                break

    def solve(self):
        self.result = None
        assignment = [None] * self.n
        available = self.counter.copy()
        # اجرای AC-2 پیش‌پردازش (قبل از شروع)
        if not self.ac2(assignment, available):
            return None
        self.backtrack(assignment, available)
        return self.result
