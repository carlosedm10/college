from scipy.optimize import linprog

# Coefficients for the objective function (costs for producing cars and storage)
costs = [
    # Costs for car type 1 in months 1, 2, 3
    4500,
    4500,
    4500,
    # Costs for car type 2 in months 1, 2, 3
    4900,
    4900,
    4900,
    # Storage costs for A and B in months 1, 2, 3
    1,
    1,
    1,
    1,
    1,
    1,
]

# The demand for each car type in each month
demand = {"car1": [50, 30, 70], "car2": [66, 35, 15]}

# The coefficients for the inequalities (machine capacity and material flow)
A_ub = [
    # Machine M1 capacity for each month
    [10, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 10, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 10, 0, 0, 7, 0, 0, 0, 0, 0, 0],
    # Machine M2 capacity for each month
    [5, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 5, 0, 0, 3, 0, 0, 0, 0, 0, 0],
]

# Upper bound constraints for machine capacity
b_ub = [
    400,
    400,
    400,  # Machine M1 capacity constraints for each month
    500,
    500,
    500,  # Machine M2 capacity constraints for each month
]

# Equality constraints for demand fulfillment
A_eq = [
    # Demand fulfillment for car type 1 each month
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # Demand fulfillment for car type 2 each month
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
]

# Equality constraints for demand quantities
b_eq = [
    demand["car1"][0],
    demand["car1"][1],
    demand["car1"][2],
    demand["car2"][0],
    demand["car2"][1],
    demand["car2"][2],
]

# Variable bounds, all variables are >= 0
bounds = [(0, None) for _ in range(len(costs))]

# Solve the linear programming problem
result = linprog(
    c=costs, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs"
)
# Extract the results
if result.success:
    production_plan = result.x[:6]  # First six are the production quantities
    storage_plan = result.x[6:]  # Last six are the storage quantities
    total_cost = result.fun
    message = result.message
    success = result.success
else:
    production_plan = None
    storage_plan = None
    total_cost = None
    message = result.message
    success = result.success

print(f"{production_plan}, {storage_plan}, {total_cost}, {message}, {success}")
