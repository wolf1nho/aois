import re

class Validator:
    def __init__(self):
        self.message = ""

    def get_message(self):
        return self.message

    def validate_expression(self, expression: str):
        expr = expression.replace(" ", "")
        if not expr:
            self.message = "Выражение пустое"
            return False
        
        allowed = set('01abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!&|~()->')
        if not all(c in allowed for c in expr):
            self.message = "Недопустимые символы в выражении"
            return False
        
        tokens = re.findall(r'[a-zA-Z]+|->|~|!|[()&|01]', expr)
        
        reconstructed = ''.join(tokens)
        if reconstructed != expr:
            self.message = "Некорректный синтаксис"
            return False
        
        stack = []
        for token in tokens:
            if token == '(':
                stack.append(token)
            elif token == ')':
                if not stack:
                    self.message = "Несбалансированные скобки"
                    return False
                stack.pop()
        if stack:
            self.message = "Несбалансированные скобки"
            return False

        variables = sorted(list(set(re.findall(r'[a-zA-Z]', expr))))
        if len(variables) > 5:
            self.message = "Слишком много переменных (максимум 5)"
            return False

        binary_ops = [t for t in tokens if t in ['&', '|', '->']]
        if len(binary_ops) > 1 and '(' not in expr and ')' not in expr:

            self.message = "Необходимо использовать скобки для связки операций"
            return False

        expects_operand = True 
        for token in tokens:
            if token.isalpha() or token in ['0', '1']:
                if not expects_operand:
                    self.message = "Неожиданная переменная"
                    return False
                expects_operand = False 
            elif token == '(':
                if not expects_operand:
                    self.message = "Неожиданная ("
                    return False
                expects_operand = True
            elif token == ')':
                if expects_operand:
                    self.message = "Неожиданная )"
                    return False
                expects_operand = False
            elif token in ['!', '&', '|', '->', '~']:
                if expects_operand:
                    if token != '!':
                        self.message = "Неожиданный бинарный оператор"
                        return False
                else:
                    if token == '!':
                        self.message = "! после операнда"
                        return False
                    expects_operand = True
            else:
                self.message = f"Неизвестный токен: {token}"
                return False
        if expects_operand:
            self.message = "Выражение заканчивается оператором"
            return False

        return True