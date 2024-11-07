import numpy as np
import json

# Example graph (costs) and parameters
graph = {
    0: {0: 0, 1: 7, 2: 6, 3: 12, 4: 8},
    1: {0: 7, 1: 0, 2: 13, 3: 9, 4: 11},
    2: {0: 6, 1: 13, 2: 0, 3: 13.6, 4: 12},
    3: {0: 13, 1: 9, 2: 13.6, 3: 0, 4: 21},
    4: {0: 8, 1: 11, 2: 12, 3: 21, 4: 0}
}
demands = [0, 5, 8, 6, 3]  # Node demands
capacity = 15  # Vehicle capacity
num_nodes = len(graph)
num_vehicles = 2

# Penalty weights (Lagrange multipliers for constraints)
lambda_single_visit = 10  # Penalty for visiting a node multiple times
lambda_capacity = 10      # Penalty for exceeding capacity
lambda_continuity = 10    # Penalty for route continuity

# Define routes as binary variables
# route[v][i][j] = 1 if vehicle v travels from node i to node j
route_vars = {(v, i, j): 0 for v in range(num_vehicles) for i in range(num_nodes) for j in range(num_nodes)}


# Initialize QUBO matrix
Q = {}

# Objective function: Minimize travel cost
for v in range(num_vehicles):
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:  # Avoid self-loops
                Q[(v, i, j)] = graph[i][j] * route_vars[(v, i, j)]


# Capacity constraint
for v in range(num_vehicles):
    capacity_penalty = 0
    for i in range(1, num_nodes):  # Exclude depot
        for j in range(num_nodes):
            capacity_penalty += demands[i] * route_vars[(v, i, j)]
    Q[(v, 'capacity')] = lambda_capacity * max(0, capacity_penalty - capacity) ** 2


def calculate_qubo_cost(route_vars, Q):
    total_cost = 0
    for (key1, key2), weight in Q.items():
        if route_vars.get(key1, 0) * route_vars.get(key2, 0) > 0:
            total_cost += weight
    return total_cost

