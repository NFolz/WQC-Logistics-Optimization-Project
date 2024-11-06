graph = {
    0: {0: 0, 1: 7, 2: 6, 3: 12, 4: 8},
    1: {0: 7, 1: 0, 2: 13, 3: 9, 4: 11},
    2: {0: 6, 1: 13, 2: 0, 3: 13.6, 4: 12},
    3: {0: 13, 1: 9, 2: 13.6, 3: 0, 4: 21},
    4: {0: 8, 1: 11, 2: 12, 3: 21, 4: 0}
}

routes = {
    1: [],
    2: [0],
    3: [0, 1,0],
    4: [0, 2,0],
    5: [0, 3,0],
    6: [0, 4,0],
    7: [0, 1, 2,0],
    8: [0, 1, 3,0],
    9: [0, 1, 4,0],
    10: [0, 2, 1,0],
    11: [0, 2, 3,0],
    12: [0, 2, 4,0],
    13: [0, 3, 1,0],
    14: [0, 3, 2,0],
    15: [0, 3, 4,0],
    16: [0, 4, 1,0],
    17: [0, 4, 2,0],
    18: [0, 4, 3,0],
    19: [0, 1, 2, 3,0],
    20: [0, 1, 2, 4,0],
    21: [0, 1, 3, 2,0],
    22: [0, 1, 3, 4,0],
    23: [0, 1, 4, 2,0],
    24: [0, 1, 4, 3,0],
    25: [0, 2, 1, 3,0],
    26: [0, 2, 1, 4,0],
    27: [0, 2, 3, 1,0],
    28: [0, 2, 3, 4,0],
    29: [0, 2, 4, 1,0],
    30: [0, 2, 4, 3,0],
    31: [0, 3, 1, 2,0],
    32: [0, 3, 1, 4,0],
    33: [0, 3, 2, 1,0],
    34: [0, 3, 2, 4,0],
    35: [0, 3, 4, 1,0],
    36: [0, 3, 4, 2,0],
    37: [0, 4, 1, 2,0],
    38: [0, 4, 1, 3,0],
    39: [0, 4, 2, 1,0],
    40: [0, 4, 2, 3,0],
    41: [0, 4, 3, 1,0],
    42: [0, 4, 3, 2,0],
    43: [0, 1, 2, 3, 4,0],
    44: [0, 1, 2, 4, 3,0],
    45: [0, 1, 3, 2, 4,0],
    46: [0, 1, 3, 4, 2,0],
    47: [0, 1, 4, 2, 3,0],
    48: [0, 1, 4, 3, 2,0],
    49: [0, 2, 1, 3, 4,0],
    50: [0, 2, 1, 4, 3,0],
    51: [0, 2, 3, 1, 4,0],
    52: [0, 2, 3, 4, 1,0],
    53: [0, 2, 4, 1, 3,0],
    54: [0, 2, 4, 3, 1,0],
    55: [0, 3, 1, 2, 4,0],
    56: [0, 3, 1, 4, 2,0],
    57: [0, 3, 2, 1, 4,0],
    58: [0, 3, 2, 4, 1,0],
    59: [0, 3, 4, 1, 2,0],
    60: [0, 3, 4, 2, 1,0],
    61: [0, 4, 1, 2, 3,0],
    62: [0, 4, 1, 3, 2,0],
    63: [0, 4, 2, 1, 3,0],
    64: [0, 4, 2, 3, 1,0],
    65: [0, 4, 3, 1, 2,0],
    66: [0, 4, 3, 2, 1,0]
}

routesDecisionVariables={}

for route_number, route in routes.items():
    # print(f"Route {route_number}: {route}")
    routesDecisionVariables[route_number]={0:1, 1:1 if 1 in route else 0, 2:1 if 2 in route else 0, 3:1 if 3 in route else 0, 4:1 if 4 in route else 0}

# print(routesDecisionVariables)

routes_cost = {}


for route_number, route in routes.items():
    cost = 0
    previous = None
    for current in route:
        if previous is not None:
            cost+= graph[previous][current]
        previous=current
    routes_cost[route_number]=cost

# print(routes_cost)
routeCost23 = 36

routeCost66 = 62.6

routeCost35 = 51

routeCost50 = 64

def testRouteCost():
    assert routeCost23 == routes_cost[23], f"Expected {routeCost23}, got {routes_cost[23]}"
    assert routeCost66 == routes_cost[66], f"Expected {routeCost66}, got {routes_cost[66]}"
    assert routeCost35 == routes_cost[35], f"Expected {routeCost35}, got {routes_cost[35]}"
    assert routeCost50 == routes_cost[50], f"Expected {routeCost50}, got {routes_cost[50]}"

testRouteCost()



fulfilledRouteCombinations = []
current_min = 150
#redundant values just to initialize array size
current_min_route_combo=[1,2]

#working function but refactoring to try and enforce QUBO Constraint of only one visit
# def routeCombinations(route_1,route_2):
    
#     oneFlag = False
#     twoFlag = False
#     threeFlag = False
#     fourFlag = False


#     if route_1[1] == 1 or route_2[1] == 1:
#         if oneFlag==True:
#             return False
#         oneFlag = True

    
#     if route_1[2] == 1 or route_2[2] == 1:
#         if twoFlag==True:
#             return False
#         twoFlag = True

   
#     if route_1[3] == 1 or route_2[3] == 1:
#         if threeFlag==True:
#             return False
#         threeFlag = True

   
#     if route_1[4] == 1 or route_2[4] == 1:
#         if fourFlag==True:
#             return False
#         fourFlag = True

#     if oneFlag and twoFlag and threeFlag and fourFlag:
#         return True
#     else:
#         return False

def routeCombinations(route_1, route_2):
    visited = set()

    # Iterate through both routes
    for node in range(1, max(route_1,route_2)):  # Nodes 1 to 4
        if route_1[node] == 1 or route_2[node] == 1:
            if node in visited:  # Check if the node has already been visited
                return False  # Duplicate visit detected
            visited.add(node)  # Mark this node as visited

    # If all nodes are visited exactly once, return True
    return len(visited) == 4

def calculateRouteCost(route_1,route_2):
    global current_min
    global current_min_route_combo
    min =routes_cost[route_1] + routes_cost[route_2]
    if(min<current_min):
        current_min= min
        current_min_route_combo[0]=route_1
        current_min_route_combo[1]=route_2
        #print(route_1,route_2)


count=0
for route_number, route in routesDecisionVariables.items():
    count2 =0
    if count==42:
        break
    for route_number_2, route_2 in routesDecisionVariables.items():
        if count2==42:
            break
        if(routeCombinations(route_2,route)):
            fulfilledRouteCombinations.append({route_number,route_number_2})
            calculateRouteCost(route_number,route_number_2)

        count2+=1
    count+=1

# print(fulfilledRouteCombinations)
print(current_min_route_combo)
print(current_min)



import json

firstRouteToSend = []
secondRouteToSend= []

for route_number,route in routes.items():
    if route_number==current_min_route_combo[0]:
        firstRouteToSend=route
    if route_number==current_min_route_combo[1]:
        secondRouteToSend=route

data_to_send = {
    "firstRouteToSend": firstRouteToSend,
    "secondRouteToSend": secondRouteToSend
}

# Write the coordinates to a JSON file
with open("testing/routes.json", "w") as file:
    #converts python objects data to JSON Format
    json.dump(data_to_send, file)

print("JSON file created: coordinates.json")




