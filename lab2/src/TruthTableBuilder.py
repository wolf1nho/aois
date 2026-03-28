import re
import itertools

from src.TruthTable import TruthTable


class TruthTableBuilder:
    @staticmethod
    def build(expression) -> TruthTable:
        expr = expression.replace(" ", "")
        variables = sorted(list(set(re.findall(r'[a-zA-Z]', expr))))
        table = TruthTable(variables=variables)

        for values in itertools.product([0, 1], repeat=len(variables)):
            state = dict(zip(variables, values))
            result = TruthTableBuilder.solve(expr, state)
            row = list(values) + [result]
            table.append(row)

        return table

    @staticmethod
    def solve(expression, variables):
        precedence = {'!': 4, '&': 3, '|': 2, '->': 1, '~': 1}

        def to_rpn(tokens):
            output = []
            stack = []
            for token in tokens:
                if token.isalpha() or token in ['0', '1']:
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


        tokens = re.findall(r'[a-zA-Z]+|->|~|!|[()&|01]', expression)
        rpn = to_rpn(tokens)

        stack = []
        for token in rpn:
            if token.isalpha():
                stack.append(variables[token])
            elif token in ['0', '1']:
                stack.append(int(token))
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