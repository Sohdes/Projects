import math


class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []


class Tree:
    def __init__(self, root):
        self.root = root

    def evaluate(self, variable_values):
        return self._evaluate_node(self.root, variable_values)

    def _evaluate_node(self, node, variable_values):
        # numeric letters
        if isinstance(node.value, (int, float)):
            return node.value
        elif isinstance(node.value, str) and node.value.startswith('x'):  # Variable lookup
            return variable_values.get(node.value, None)
        elif node.value in ['+', '-', '*', '/', '**']:  # Arithmetic operations
            operands = [self._evaluate_node(child, variable_values) for child in node.children]
            return self.apply_operator(node.value, operands)
        elif node.value in ['sin', 'cos', 'tanh']:  # Mathematical functions
            operand = self._evaluate_node(node.children[0], variable_values)
            return self.apply_function(node.value, operand)

    # describe functions
    def apply_operator(self, operator, operands):
        if operator == '+':
            return sum(operands)
        elif operator == '-':
            return operands[0] - sum(operands[1:])
        elif operator == '*':
            result = 1
            for operand in operands:
                result *= operand
            return result
        elif operator == '/':
            result = operands[0]
            for operand in operands[1:]:
                if operand == 0:
                    return float('inf')
                result /= operand
            return result
        elif operator == '**':
            return operands[0] ** operands[1]
    # describe functions
    def apply_function(self, func, operand):
        if func == 'sin':
            return math.sin(operand)
        elif func == 'cos':
            return math.cos(operand)
        elif func == 'tanh':
            return math.tanh(operand)





m = int(input("Enter number of Trees (outputs): "))
n = int(input("Enter number of variables: "))

variables = {}
for i in range(1,n+1):
    variable = input(f"Enter variable x{i} and its value(like:x1 14): ").split()
    variables[variable[0]] = int(variable[1])

trees = []
for j in range(1,m+1):
    extree = input(f"Enter tree{j}(like: Node('**',[Node('x1'),Node(8)])): ")
    tree = eval(extree)
    trees.append(Tree(tree))

for h, tree in enumerate(trees):
    output = tree.evaluate(variables)
    print(f"Result of f{h + 1}: {output}")


