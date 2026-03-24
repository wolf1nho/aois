import re
import itertools

from numpy import stack

class TruthTableBuilder:
    def __init__(self):
        self.table = []
        self.variables = []

    def validate_expression(self, expression):
        expr = expression.replace(" ", "")
        if not expr:
            return False, "Выражение пустое"
        
        allowed = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!&|~()->')
        if not all(c in allowed for c in expr):
            return False, "Недопустимые символы в выражении"
        
        tokens = re.findall(r'[a-zA-Z]+|->|~|!|[()&|]', expr)
        
        reconstructed = ''.join(tokens)
        if reconstructed != expr:
            return False, "Некорректный синтаксис"
        
        stack = []
        for token in tokens:
            if token == '(':
                stack.append(token)
            elif token == ')':
                if not stack:
                    return False, "Несбалансированные скобки"
                stack.pop()
        if stack:
            return False, "Несбалансированные скобки"

        self.variables = sorted(list(set(re.findall(r'[a-zA-Z]', expr))))
        if len(self.variables) > 5:
            return False, "Слишком много переменных (максимум 5)"

        # Требуем хотя бы одну пару скобок, если в выражении более одного бинарного оператора
        binary_ops = [t for t in tokens if t in ['&', '|', '->']]
        if len(binary_ops) > 1 and '(' not in expr and ')' not in expr:
            return False, "Необходимо использовать скобки для связки операций"

        expects_operand = True 
        for token in tokens:
            if token.isalpha():
                if not expects_operand:
                    return False, "Неожиданная переменная"
                expects_operand = False 
            elif token == '(':
                if not expects_operand:
                    return False, "Неожиданная ("
                expects_operand = True
            elif token == ')':
                if expects_operand:
                    return False, "Неожиданная )"
                expects_operand = False
            elif token in ['!', '&', '|', '->', '~']:
                if expects_operand:
                    if token != '!':
                        return False, "Неожиданный бинарный оператор"
                else:
                    if token == '!':
                        return False, "! после операнда"
                    expects_operand = True
            else:
                return False, f"Неизвестный токен: {token}"
        if expects_operand:
            return False, "Выражение заканчивается оператором"
        
        return True, ""

    def build(self, expression) -> list[list[bool]]:
        valid, msg = self.validate_expression(expression)
        if not valid:
            print(f"Ошибка валидации: {msg}")
            return []
        
        expr = expression.replace(" ", "")
        variables = sorted(list(set(re.findall(r'[a-zA-Z]', expr))))
        self.table = []

        for values in itertools.product([0, 1], repeat=len(variables)):
            state = dict(zip(variables, values))
            result = self.solve(expr, state)
            row = list(values) + [result]
            self.table.append(row)

        return self.table

    def solve(self, expression, variables):
        precedence = {'!': 4, '&': 3, '|': 2, '->': 1, '~': 1}

        def to_rpn(tokens):
            output = []
            stack = []
            for token in tokens:
                if token.isalpha():
                    output.append(token)
                elif token == '(':
                    stack.append(token)
                elif token == ')':
                    while stack and stack[-1] != '(':
                        output.append(stack.pop())
                    stack.pop()
                else:
                    while stack and stack[-1] != '(' and \
                          precedence.get(stack[-1], 0) >= precedence.get(token, 0):
                        output.append(stack.pop())
                    stack.append(token)
            while stack:
                output.append(stack.pop())
            return output


        tokens = re.findall(r'[a-zA-Z]+|->|~|!|[()&|]', expression)
        rpn = to_rpn(tokens)

        stack = []
        for token in rpn:
            if token.isalpha():
                stack.append(variables[token])
            elif token == '!':
                val = stack.pop()
                stack.append(1 - val)
            elif token == '&':
                b, a = stack.pop(), stack.pop()
                stack.append(a * b)
            elif token == '|':
                b, a = stack.pop(), stack.pop()
                stack.append(a + b - a * b)
            elif token == '->':
                b, a = stack.pop(), stack.pop()
                stack.append((1 - a) + b - (1 - a) * b)
            elif token == '~':
                b, a = stack.pop(), stack.pop()
                stack.append(a * b + (1 - a) * (1 - b))

        return stack[0]
    
    def print_table(self, expression, table):
        if not table:
            return
        variables = sorted(list(set(re.findall(r'[a-zA-Z]', expression.replace(" ", "")))))
        header = "  ".join(variables) + " | " + expression
        print(header)
        print("-" * len(header))
        for row in table:
            v_str = "  ".join(str(int(v)) for v in row[:-1])
            print(f"{v_str} | {int(bool(row[-1]))}")