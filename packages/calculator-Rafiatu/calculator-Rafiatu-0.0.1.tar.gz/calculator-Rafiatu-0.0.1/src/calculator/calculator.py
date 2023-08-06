class Calculator:
    def __init__(self):
        self.val = 0

    def add(self, num):
        self.val += num
        return self.val

    def subtract(self, num):
        self.val -= num
        return self.val

    def multiply(self, num):
        self.val *= num
        return self.val

    def divide(self, num):
        try:
            self.val /= num
            return self.val
        except ZeroDivisionError:
            return f'{num} cannot be divided by zero'

    def root(self, n):
        self.val **= (1/n)
        return self.val

    def reset_memory(self):
        self.val = 0
        return self.val
