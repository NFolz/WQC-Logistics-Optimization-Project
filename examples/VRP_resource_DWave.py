from dwave.system import LeapHybridNLSampler
# from dwave.system import DWaveSampler, EmbeddingComposite
from dwave.optimization.generators import capacitated_vehicle_routing # https://docs.ocean.dwavesys.com/en/stable/docs_optimization/reference/generators.html#dwave.optimization.generators.capacitated_vehicle_routing
# import dwave.inspector
from dimod import *
# import numpy as np
import random
import time
from dotenv import load_dotenv
import os

load_dotenv()

startTime=time.time()

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

demandGoogle = [0, 10, 20, 20, 40, 10, 50, 10, 5, 5]
sitesGoogle= [
    (43.65107, -79.347015),  # Depot (Toronto)
    (43.648883, -79.375395),  # Location 1
    (43.676618, -79.410064),  # Location 2
    (43.689533, -79.298968),  # Location 3
    (43.654425, -79.380749),  # Location 4
    (43.629310, -79.352850),  # Location 5
    (43.718403, -79.518892),  # Location 6
    (43.729432, -79.265549),  # Location 7
    (43.657217, -79.463760),  # Location 8
    (43.652607, -79.384223),  # Location 9
]

#demandGoogle, sitesGoogle = generate_vrp_data() #generating the demand and sites for the vrp
print("Demand:", demandGoogle)
print("Sites:", sitesGoogle)

model = capacitated_vehicle_routing( #using the dwave library to model the VRP using the generated data
    demand=demandGoogle,
    number_of_vehicles=2,
    vehicle_capacity=150,
    locations_x=[x for x,y in sitesGoogle],
    locations_y=[y for x,y in sitesGoogle])

# For the token, create a .env file in the root directory and add your token (DWAVELEAP_TOKEN=your_token)
sampler = LeapHybridNLSampler(token=os.getenv('DWAVELEAP_TOKEN')) #specifying the type of solver we are going to submit our problem to
results = sampler.sample( #creating an object to store the results of the computation
    model, #model as the input
    time_limit=10) #maximum time we want to allow the solver to use

num_samples = model.states.size()
route, = model.iter_decisions()                     
route1, route2 = route.iter_successors()    
endTime = time.time()
elapsedTime=endTime-startTime      
print(f"Elapsed time: {elapsedTime:.2f} seconds")  
for i in range(min(3, num_samples)):
    print(f"Objective value {int(model.objective.state(i))} for \n" \
    f"\t Route 1: {route1.state(i)} \t Route 2: {route2.state(i)} \n" \
    f"\t Feasible: {all(sym.state(i) for sym in model.iter_constraints())}")


