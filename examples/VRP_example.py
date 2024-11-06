import itertools

def create_vrp_qubo_biases(n_customers, k_vehicles, max_capacity, demands, costs):
    # Initialize dictionaries for biases
    linear_dict = {}
    quad_dict = {}
    
    # Variable to index mappings for the QUBO variables
    var_to_idx = {(v, i, p): idx for idx, (v, i, p) in enumerate(
                  (v, i, p) for v in range(1, k_vehicles + 1) for i in range(n_customers + 1) for p in range(1, n_customers + 1))}
    
    # Reverse dictionary for human-readable output
    idx_to_var = {idx: (v, i, p) for (v, i, p), idx in var_to_idx.items()}
    
    # Objective Function: Minimize traversal costs
    for v in range(1, k_vehicles + 1):
        for i in range(n_customers + 1):
            for j in range(n_customers + 1):
                if i != j:
                    for p in range(1, n_customers):
                        # Add to quadratic dictionary with traversal cost as bias
                        idx1 = var_to_idx[(v, i, p)]
                        idx2 = var_to_idx[(v, j, p + 1)]
                        quad_dict[(idx1, idx2)] = costs.get((i, j), 0)

    # Constraints as linear terms (example bias values)
    for i in range(1, n_customers + 1):
        for p in range(1, n_customers + 1):
            idx = var_to_idx[(1, i, p)]  # Example for vehicle 1
            linear_dict[idx] = -1  # Bias placeholder


    # Translate the dictionaries for readability
    readable_linear_dict = {f"x_{idx_to_var[idx][0]}_{idx_to_var[idx][1]}_{idx_to_var[idx][2]}": bias
                            for idx, bias in linear_dict.items()}
    
    readable_quad_dict = {f"(x_{idx_to_var[idx1][0]}_{idx_to_var[idx1][1]}_{idx_to_var[idx1][2]}, "
                          f"x_{idx_to_var[idx2][0]}_{idx_to_var[idx2][1]}_{idx_to_var[idx2][2]})": bias
                          for (idx1, idx2), bias in quad_dict.items()}

    return readable_linear_dict, readable_quad_dict, var_to_idx


import random

def generate_random_vrp_inputs(n_customers, k_vehicles, max_demand=10, max_cost=20, max_capacity=None):
    """
    Generates random inputs for the Capacitated Vehicle Routing Problem (CVRP).
    
    Parameters:
        n_customers (int): Number of customers (excluding depot).
        k_vehicles (int): Number of vehicles.
        max_demand (int): Maximum demand for a customer.
        max_cost (int): Maximum cost for traversing an edge.
        max_capacity (int or None): Vehicle capacity. If None, it will be set to the sum of random demands divided by the number of vehicles.
    
    Returns:
        tuple: Randomly generated parameters:
            - Vehicle capacity (int)
            - List of demands for each customer (list)
            - Dictionary of costs for edges between each pair of nodes (dict)
    """
    
    # Generate random demands for each customer (node 1 to n_customers, excluding depot)
    demands = [random.randint(1, max_demand) for _ in range(n_customers)]
    
    # Generate random costs for each edge between nodes (including the depot as node 0)
    costs = {}
    for i in range(n_customers + 1):
        for j in range(i + 1, n_customers + 1):
            cost = random.randint(1, max_cost)
            costs[(i, j)] = cost
            costs[(j, i)] = cost  # Assume undirected graph with symmetric costs
    
    # Set vehicle capacity if not provided, based on total demand
    if max_capacity is None:
        max_capacity = sum(demands) // k_vehicles
    
    return max_capacity, demands, costs

n_customers = 6
n_vehicles = 2
max_capacity, demands, costs = generate_random_vrp_inputs(n_customers, n_vehicles)
print("Vehicle Capacity:", max_capacity)
print("Customer Demands:", demands)
print("Traversal Costs:", costs)

linear_dict, quad_dict, var_to_idx = create_vrp_qubo_biases(n_customers, n_vehicles, max_capacity, demands, costs)
print("Linear dict:", linear_dict)
print("Quadratic dict:",quad_dict)
print("Variable Mapping:", var_to_idx)

from dwave.system import DWaveSampler, EmbeddingComposite
from greedy import SteepestDescentSolver
import dwave.inspector
import dimod
sampler = EmbeddingComposite(DWaveSampler(token="DEV-edba7dbb3a72fc17fe9561831ed5792ddea6c5b2"))
Q = {**linear_dict, **quad_dict}
print("Q dictionary structure:")
for key, value in Q.items():
    print(key, value)
bqm = dimod.BinaryQuadraticModel.from_qubo(Q)
sampleset_qc = sampler.sample(bqm, num_reads=500)
print("Original sampleset from quantum computer:")
print(sampleset_qc)
dwave.inspector.show(sampleset_qc)
solver_greedy = SteepestDescentSolver()
sampleset_pp = solver_greedy.sample(bqm, initial_states=sampleset_qc)
print("Post-processed sampleset using SteepestDescentSolver:")
print(sampleset_pp)
