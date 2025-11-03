import math

class Node:
    # childern=None: no leaf and value
    def __init__(self, value, children=None):
        self.value = value
        self.children = children

class Tree:
    def __init__(self, root):
        self.root = root
    # Basic node is None then is root
    def computing(self, node=None):
        if node is None:
            node = self.root
        # Return the leaves
        if isinstance(node.value, (int, float)):
            return node.value
        elif node.value in ['+', '-', '*', '/']:
            return self.operator(node.value, [self.computing(child) for child in node.children])
        elif node.value in ['sin', 'cos', 'tanh']:
            return self.function(node.value, self.computing(node.children[0]))
    # Define oprators
    def operator(self, operator, operands):
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
                result /= operand
            return result

    # Define functions
    def function(self, func, operand):
        if func == 'sin':
            return math.sin(operand)
        elif func == 'cos':
            return math.cos(operand)
        elif func == 'tanh':
            return math.tanh(operand)
x,y = 0,8
root = Node('+', [Node('*',[Node(2),Node(math.pi)]),Node('-',[Node('+',[Node(x),Node(3)]),Node('/',[Node(y),Node('+',[Node(5),Node(1)])])])] )
tree = Tree(root)
output = tree.computing()
print(f"Output: {output}")
