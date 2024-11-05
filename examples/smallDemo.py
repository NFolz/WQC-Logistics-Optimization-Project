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
