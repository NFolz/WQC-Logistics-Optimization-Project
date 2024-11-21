import googlemaps
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import time

# Google Maps API Key
API_KEY = ""

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=API_KEY)

# Define locations (latitude, longitude) including a depot (first location)
locations = [
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

# Define the demand for each location (first value is the depot with no demand)
demand = [0, 10, 20, 20, 40, 10, 50, 10, 5, 5]  # Example demands for each location

# Function to generate a distance matrix using Google Maps API
def create_distance_matrix(locations):
    print("Fetching distance matrix from Google Maps...")
    matrix = []
    for origin in locations:
        response = gmaps.distance_matrix(origins=[origin], destinations=locations, mode="driving")
        distances = [row['distance']['value'] for row in response['rows'][0]['elements']]
        matrix.append(distances)
    return matrix

# VRP Solver function
def solve_vrp(distance_matrix, num_vehicles, capacity):
    print("Solving VRP...")
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, 0)
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of travel
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add demand constraints (capacity constraint)
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return demand[from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

    # Set capacity constraints (vehicle capacity)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        [capacity] * num_vehicles,  # Vehicle capacity
        True,  # Start cumul to zero
        "Capacity"
    )

    # Set search parameters
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    # Solve the problem
    solution = routing.SolveWithParameters(search_params)
    return routing, manager, solution

# Display solution
def print_solution(manager, routing, solution):
    print("Routes:")
    total_distance = 0
    for vehicle_id in range(manager.GetNumberOfVehicles()):
        index = routing.Start(vehicle_id)
        route_distance = 0
        route = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append(node_index)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        route.append(manager.IndexToNode(index))
        print(f"Vehicle {vehicle_id}: {route} - Distance: {route_distance} meters")
        total_distance += route_distance
    print(f"Total distance: {total_distance} meters")

# Main function
def main():
    # Start timer
    start_time = time.time()

    # Create the distance matrix
    distance_matrix = create_distance_matrix(locations)

    # Number of vehicles and vehicle capacity
    num_vehicles = 2
    vehicle_capacity = 150  # Maximum capacity of each vehicle

    # Solve VRP
    routing, manager, solution = solve_vrp(distance_matrix, num_vehicles, vehicle_capacity)

    # End timer
    end_time = time.time()

    # Display results
    if solution:
        print_solution(manager, routing, solution)
    else:
        print("No solution found!")

    print(f"Execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()

