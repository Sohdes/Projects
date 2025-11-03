import random
import math
import numpy as np

# Define divide
def protected_div(left, right):
    if right == 0:
        return 1
    return left / right


# Define Square
def safe_sqrt(x):
    if x < 0:
        return 0
    return math.sqrt(x)


# Define oprations
primitive_set = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': protected_div,
    'cos': math.cos,
    'sin': math.sin,
    'tanh': math.tanh,
    'sqrt': safe_sqrt
}


def generate_random_functions(max_depth, current_depth=0):
    func = random.choice(list(primitive_set.keys()))
    if current_depth < max_depth:
        if func in ['+', '-', '*', '/']:
            return f'({generate_random_functions(max_depth, current_depth + 1)} {func} {generate_random_functions(max_depth, current_depth + 1)})'
        elif func in ['cos', 'sin', 'sqrt','tanh']:
            return f'{func}({generate_random_functions(max_depth, current_depth + 1)})'
    return 'x'


# Execute function h
def eval_expression(expr, x):
    #__builtins__: security
    return eval(expr, {"__builtins__": None}, {'x': x, 'cos': math.cos, 'sin': math.sin, 'sqrt': safe_sqrt, 'tanh': math.tanh})


def fitness(expr, points):
    try:
        return sum((eval_expression(expr, x) - y) ** 2 for x, y in points) / 2*(len(points))
    except:
        return float('inf')


def selection(population):
    selected = min((population), key=lambda ind: ind[1])
    return selected


def find_operations(expr):
    ops_positions = []
    i = 0
    while i < len(expr):
        for op in operations:
            if expr[i:i+len(op)] == op:
                ops_positions.append((i, op))
                # Continue
                i += len(op) - 1
                break
        i += 1
    return ops_positions


def replace_random_operation(expr):
    ops_positions = find_operations(expr)
    if not ops_positions:
        return expr  # No operation to replace
    index, op_to_replace = random.choice(ops_positions)
    new_op = random.choice([op for op in operations if op != op_to_replace])
    new_expr = expr[:index] + new_op + expr[index + len(op_to_replace):]
    return new_expr


# Randomly choise a replaced function
def crossover(ind1, ind2):
    new_ind1 = replace_random_operation(ind1)
    new_ind2 = replace_random_operation(ind2)
    return random.choice([new_ind1, new_ind2])


def mutation(expr):
    new_expr = replace_random_operation(expr)
    return new_expr


def GA(data_points, population_size=80, generations=30, max_depth=5):
    # Make list of functions with flout inf
    population = [(generate_random_functions(max_depth), float('inf')) for _ in range(population_size)]

    # Replace value of fitness value to inf
    population = [(expr, fitness(expr, data_points)) for expr, _ in population]

    for generation in range(generations):
        new_population = []
        for _ in range(population_size):
            ind1 = selection(population)
            ind2 = selection(population)
            new_expr = crossover(ind1[0], ind2[0])
            new_expr = mutation(new_expr)
            new_population.append((new_expr, fitness(new_expr, data_points)))
        population = sorted(new_population, key=lambda ind: ind[1])[:population_size]
    best_function = min(population, key=lambda ind: ind[1])
    return best_function


operations = ['+', '-', '*', '/', 'cos', 'sin', 'sqrt', 'tanh']
np.seterr(divide='ignore', invalid='ignore')


def load_data(path):
    return np.loadtxt(path)

x_file_path = "./X.txt"
y_file_path = "./y.txt"




X = load_data(x_file_path)
y = load_data(y_file_path)

import matplotlib.pyplot as plt

data_points = list(zip(X, y))

best_function = GA(data_points)
print("Best function:", best_function[0])
print()

Function = best_function[0]
# X values for Function
x_values = np.linspace(min(X), max(X), 80)
# Range of Function
y_values = [eval_expression(Function, x) for x in x_values]

# Plot for actual data
plt.scatter(X, y, color='blue', label='Actual Data')
# Plot for Function
plt.plot(x_values, y_values, color='red', label='Best Function')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Best Function vs Actual Data')
plt.legend()

# Show the plot
plt.show()

