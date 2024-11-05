from dwave.system import LeapHybridNLSampler
from dwave.system import DWaveSampler, EmbeddingComposite
from dwave.optimization.generators import capacitated_vehicle_routing
import dwave.inspector
from dimod import *
import numpy as np
import random


def generate_vrp_data(num_sites=10, demand_range=(10, 70), coord_range=(-100, 100)): # generates random data for the VRP
    """
    Parameters:
        num_sites (int): The number of sites (excluding the depot).
        demand_range (tuple): The range (min, max) for generating random demand values.
        coord_range (tuple): The range (min, max) for generating random site coordinates.
        
    Returns:
        tuple: A tuple containing:
            - demand (list of int): List of demands for each site, with 0 as the first item for the depot.
            - sites (list of tuples): List of (x, y) coordinates for each site, including the depot.
    """
    
    # Generate demand with the first value set to 0 for the depot
    demand = [0] + [random.randint(demand_range[0], demand_range[1]) for _ in range(num_sites)]
    
    # Generate coordinates for each site, including the depot at (0,0) or a random position
    depot = (0, 0)
    sites = [depot] + [(random.randint(coord_range[0], coord_range[1]), 
                        random.randint(coord_range[0], coord_range[1])) for _ in range(num_sites)]
    
    return demand, sites

demand, sites = generate_vrp_data() #generating the demand and sites for the vrp
print("Demand:", demand)
print("Sites:", sites)

model = capacitated_vehicle_routing( #using the dwave library to model the VRP using the generated data
    demand=demand,
    number_of_vehicles=2,
    vehicle_capacity=300,
    locations_x=[x for x,y in sites],
    locations_y=[y for x,y in sites])

sampler = LeapHybridNLSampler(token="DEV-edba7dbb3a72fc17fe9561831ed5792ddea6c5b2") #specifying the type of solver we are going to submit our problem to
results = sampler.sample( #creating an object to store the results of the computation
    model, #model as the input
    time_limit=10) #maximum time we want to allow the solver to use

num_samples = model.states.size()
route, = model.iter_decisions()                     
route1, route2 = route.iter_successors()            
for i in range(min(3, num_samples)):
    print(f"Objective value {int(model.objective.state(i))} for \n" \
    f"\t Route 1: {route1.state(i)} \t Route 2: {route2.state(i)} \n" \
    f"\t Feasible: {all(sym.state(i) for sym in model.iter_constraints())}")







