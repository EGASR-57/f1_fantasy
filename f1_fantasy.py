from pulp import LpMaximize, LpProblem, LpVariable, lpSum

# Define arrays
drivers = [
    "Jack Doohan", "Pierre Gasly", "Fernando Alonso", "Lance Stroll", 
    "Charles Leclerc", "Lewis Hamilton", "Esteban Ocon", "Oliver Bearman", 
    "Lando Norris", "Oscar Piastri", "Andrea Kimi Antonelli", "George Russell", 
    "Isack Hadjar", "Yuki Tsunoda", "Max Verstappen", "Liam Lawson", 
    "Gabriel Bortoleto", "Nico Hulkenberg", "Alexander Albon", "Carlos Sainz Jr."
]
driver_costs = [
    6, 10.6, 7.6, 9.3,
    25.3, 23.6, 8.1, 6.7, 
    29.6, 23, 19.3, 21.4,
    5, 8.4, 28.6, 16.8, 
    4.8, 7.6, 12.8, 11.9
]
driver_points = [
    -9, -7, -36, 33,
    0, 3, 32, 22, 
    100, 55, 61, 60,
    -9, 6, 59, 5, 
    -11, 22, 28, -11
]

constructors = [
    "Alpine", "Aston Martin", "Ferrari", "Haas", "McLaren", 
    "Mercedes", "Racing Bulls", "Red Bull", "Kick Sauber", "Williams"
]
constructor_costs = [
    8.3, 7.3, 27.1, 8.2, 30.6, 
    23.3, 8, 25.4, 6.2, 13.5
]
constructor_points = [
    -20, 5, 13, 61, 172, 
    136, 32, 86, 15, 36
]

# Create the optimization problem
prob = LpProblem("F1_Fantasy_Team", LpMaximize)

# Define binary variables (1 if selected, 0 if not)
driver_vars = [LpVariable(f"driver_{i}", cat="Binary") for i in range(len(drivers))]
constructor_vars = [LpVariable(f"constructor_{i}", cat="Binary") for i in range(len(constructors))]

# Objective: Maximize total expected points
prob += lpSum([driver_points[i] * driver_vars[i] for i in range(len(drivers))] + 
              [constructor_points[i] * constructor_vars[i] for i in range(len(constructors))])

# Constraint 1: Total cost <= 100 million
prob += lpSum([driver_costs[i] * driver_vars[i] for i in range(len(drivers))] + 
              [constructor_costs[i] * constructor_vars[i] for i in range(len(constructors))]) <= 100

# Constraint 2: Exactly 5 drivers
prob += lpSum(driver_vars) == 5

# Constraint 3: Exactly 2 constructors
prob += lpSum(constructor_vars) == 2

# Solve the problem
prob.solve()

# Output the selected team
print("Your Optimized F1 Fantasy Team:")
print("\nDrivers:")
total_cost = 0
total_points = 0
for i in range(len(drivers)):
    if driver_vars[i].varValue == 1:
        print(f"{drivers[i]} - Cost: ${driver_costs[i]}m, Points: {driver_points[i]}")
        total_cost += driver_costs[i]
        total_points += driver_points[i]

print("\nConstructors:")
for i in range(len(constructors)):
    if constructor_vars[i].varValue == 1:
        print(f"{constructors[i]} - Cost: ${constructor_costs[i]}m, Points: {constructor_points[i]}")
        total_cost += constructor_costs[i]
        total_points += constructor_points[i]

print(f"\nTotal Cost: ${total_cost:.2f}m")
print(f"Total Expected Points: {total_points}")
