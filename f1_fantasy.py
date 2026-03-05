from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value

# 1. DATA: 2026 Official Pricing & Market Valuation
drivers = [
    "Verstappen", "Russell", "Norris", "Piastri", "Antonelli", 
    "Leclerc", "Hamilton", "Hadjar", "Gasly", "Sainz", 
    "Albon", "Alonso", "Stroll", "Bearman", "Ocon", 
    "Hulkenberg", "Lawson", "Bortoleto", "Lindblad", "Colapinto",
    "Pérez", "Bottas"
]
costs = [
    27.7, 27.4, 27.2, 25.5, 23.2, 22.8, 22.5, 15.1, 12.0, 11.8,
    11.6, 10.0, 8.0, 7.4, 7.3, 6.8, 6.5, 6.4, 6.2, 6.2, 6.0, 5.9
]

constructors = [
    "Mercedes", "McLaren", "Red Bull", "Ferrari", "Alpine",
    "Williams", "Aston Martin", "Haas", "Audi", "Racing Bulls", "Cadillac"
]
c_costs = [29.3, 28.9, 28.2, 23.3, 12.5, 12.0, 10.3, 7.4, 6.6, 6.3, 6.0]

# Initialize Problem
prob = LpProblem("F1_Fantasy_Multi_Solution", LpMaximize)

# 2. VARIABLES
d_vars = [LpVariable(f"d_{i}", cat="Binary") for i in range(len(drivers))]
c_vars = [LpVariable(f"c_{i}", cat="Binary") for i in range(len(constructors))]
# DRS Boost: One of the 5 selected drivers gets 2x points
drs_vars = [LpVariable(f"drs_{i}", cat="Binary") for i in range(len(drivers))]

# 3. OBJECTIVE: Maximize total value (Points = Cost)
# Note: DRS boost adds the value of the driver one extra time (Total = 2x)
prob += lpSum([costs[i] * d_vars[i] for i in range(len(drivers))] + 
              [costs[i] * drs_vars[i] for i in range(len(drivers))] + 
              [c_costs[j] * c_vars[j] for j in range(len(constructors))])

# 4. CONSTRAINTS
prob += lpSum([costs[i] * d_vars[i] for i in range(len(drivers))] + 
              [c_costs[j] * c_vars[j] for j in range(len(constructors))]) <= 100
prob += lpSum(d_vars) == 5
prob += lpSum(c_vars) == 2
prob += lpSum(drs_vars) == 1
for i in range(len(drivers)):
    prob += drs_vars[i] <= d_vars[i] # Can only boost a selected driver

# 5. LOOP TO FIND TOP 5 SOLUTIONS
print(f"{'Rank':<5} | {'Total Value':<12} | {'Team Composition'}")
print("-" * 80)

for rank in range(1, 6):
    prob.solve()
    if prob.status != 1: break
    
    # Extract results
    sel_drivers = [drivers[i] for i in range(len(drivers)) if d_vars[i].varValue == 1]
    sel_consts = [constructors[j] for j in range(len(constructors)) if c_vars[j].varValue == 1]
    drs_name = [drivers[i] for i in range(len(drivers)) if drs_vars[i].varValue == 1][0]
    
    total_val = sum(costs[drivers.index(d)] for d in sel_drivers) + \
                sum(c_costs[constructors.index(c)] for c in sel_consts)
    
    print(f"#{rank:<4} | ${total_val:>10.1f}m | {', '.join(sel_drivers)} + {', '.join(sel_consts)} (DRS: {drs_name})")

    # Add Integer Cut: Force the solver to find a DIFFERENT combination of 5 drivers + 2 constructors
    # We sum the variables that are currently 1; next solution must have at least one change.
    curr_d_idx = [i for i in range(len(drivers)) if d_vars[i].varValue == 1]
    curr_c_idx = [j for j in range(len(constructors)) if c_vars[j].varValue == 1]
    
    prob += lpSum([d_vars[i] for i in curr_d_idx] + [c_vars[j] for j in curr_c_idx]) <= 6