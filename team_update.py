from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value

# 1. INPUT DATA (Update these after each race)
drivers = ["Verstappen", "Russell", "Antonelli", "Leclerc",
           "Hamilton", "Norris", "Bearman", "Lindblad",
           "Bortoleto", "Gasly", "Sainz", "Ocon",
           "Albon", "Colapinto", "Lawson", "Perez",
           "Hadjar", "Piastri", "Alonso", "Bottas", "Hulkenberg", "Stroll"]

driver_costs = [28.0, 27.7, 23.5, 23.1,
                22.6, 27.1, 8.0, 6.8,
                7.0, 12.2, 11.6, 7.9,
                11.4, 6.4, 6.3, 5.8,
                14.5, 25.2, 9.4, 5.3, 6.2, 7.4]

driver_points = [
    50, 39, 32, 29,
    25, 21, 20, 15,
    13, 11, 9, 9,
    8, 6, 5, 4,
    -8, -14, -14, -16, -20, -23
]

constructors = ["Mercedes", "Ferrari", "Red Bull Racing", "Racing Bulls", "Haas",
                "Alpine", "Williams", "McLaren", "Audi", "Cadillac"]
constructor_costs = [29.6, 23.6, 28.5, 6.9, 8.0,
                     13.1, 12.6, 28.8, 6.0, 5.4, 9.7]
constructor_points = [
    96, 69, 42, 35, 34, 22,
    20, 19, 0, -13, -38
]

# 2. CURRENT TEAM CONFIGURATION
# Mark which drivers/constructors you currently have (1 for yes, 0 for no)
current_drivers = []
for i in drivers:
    if i in ["Verstappen", "Hamilton", "Hadjar", "Sainz", "Alonso"]:
        current_drivers.append(1)
    else:
        current_drivers.append(0)
current_constructors = []
for j in constructors:
    if j in ["Audi", "Racing Bulls"]:
        current_constructors.append(1)
    else:
        current_constructors.append(0)

FREE_TRANSFERS = 2  # Set to 2 or 3 depending on your bank
BUDGET = 101.5      # Update this as your team value grows!

# 3. DEFINE THE PROBLEM
prob = LpProblem("F1_Transfer_Optimizer", LpMaximize)

# Variables
d_vars = [LpVariable(f"d_{i}", cat="Binary") for i in range(len(drivers))]
c_vars = [LpVariable(f"c_{i}", cat="Binary") for i in range(len(constructors))]

# Transfer Tracking Variables
# 'change' is 1 if we sell/buy a new asset
d_change = [LpVariable(f"d_ch_{i}", cat="Binary") for i in range(len(drivers))]
c_change = [LpVariable(f"c_ch_{i}", cat="Binary") for i in range(len(constructors))]

# Penalties (Extra transfers cost 10 points each)
total_changes = lpSum(d_change) + lpSum(c_change)
extra_transfers = LpVariable("extra_transfers", lowBound=0, cat="Integer")
prob += extra_transfers >= (total_changes / 2) - FREE_TRANSFERS # Each swap is 2 changes (1 out, 1 in)

# 4. OBJECTIVE: Points - (Extra Transfer Penalty)
prob += lpSum([driver_points[i] * d_vars[i] for i in range(len(drivers))] + 
              [constructor_points[j] * c_vars[j] for j in range(len(constructors))]) - (extra_transfers * 10)

# 5. CONSTRAINTS
prob += lpSum([driver_costs[i] * d_vars[i] for i in range(len(drivers))] + 
              [constructor_costs[j] * c_vars[j] for j in range(len(constructors))]) <= BUDGET
prob += lpSum(d_vars) == 5
prob += lpSum(c_vars) == 2

# Link change variables: if current != new, change = 1
for i in range(len(drivers)):
    prob += d_change[i] >= d_vars[i] - current_drivers[i]
    prob += d_change[i] >= current_drivers[i] - d_vars[i]

for j in range(len(constructors)):
    prob += c_change[j] >= c_vars[j] - current_constructors[j]
    prob += c_change[j] >= current_constructors[j] - c_vars[j]

# 6. SOLVE & PRINT
prob.solve()

print(f"Status: {prob.status}")
print(f"Total Team Value Score: {value(prob.objective) + (extra_transfers.varValue * 10)}")
print(f"Transfers Required: {int(sum(d_change[i].varValue for i in range(len(drivers))) + sum(c_change[j].varValue for j in range(len(constructors)))) / 2}")
print(f"Penalty Incurred: -{extra_transfers.varValue * 10} points\n")

print("OPTIMIZED LINEUP:")
for i in range(len(drivers)):
    if d_vars[i].varValue == 1:
        status = "[STAY]" if current_drivers[i] == 1 else "[NEW]"
        print(f"{status} Driver: {drivers[i]}")
for j in range(len(constructors)):
    if c_vars[j].varValue == 1:
        status = "[STAY]" if current_constructors[j] == 1 else "[NEW]"
        print(f"{status} Constructor: {constructors[j]}")