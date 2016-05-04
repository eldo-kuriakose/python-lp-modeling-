"""
The Beer Distribution Problem for the PuLP Modeller
Authors: Antony Phillips, Dr Stuart Mitchell  2007
"""

# Import PuLP modeler functions
from pulp import *

# Creates a list of all the supply nodes
Warehouses = ["A", "B"]

# Creates a dictionary for the number of units of supply for each supply node
supply = {"A": 70,
          "B": 40}

# Creates a list of all demand nodes
TruckStops = ["1", "2", "3"]

# Creates a dictionary for the number of units of demand for each demand node
demand = {"1":40,
          "2":35,
          "3":25
          }

# Creates a list of costs of each transportation path
costs = [   #Bars
         #1 2 3 4 5
         [8,6,3],#A   Warehouses
         [2,4,9] #B
         ]

# The cost data is made into a dictionary
costs = makeDict([Warehouses,TruckStops],costs,0)

# Creates the 'prob' variable to contain the problem data
prob = LpProblem("Oil Distribution Problem",LpMinimize)

# Creates a list of tuples containing all the possible routes for transport
Routes = [(w,b) for w in Warehouses for b in TruckStops]

# A dictionary called 'Vars' is created to contain the referenced variables(the routes)
vars = LpVariable.dicts("Route",(Warehouses,TruckStops),0,None,LpInteger)

# The objective function is added to 'prob' first
prob += lpSum([vars[w][b]*costs[w][b] for (w,b) in Routes]), "Sum_of_Transporting_Costs"

# The supply maximum constraints are added to prob for each supply node (warehouse)
for w in Warehouses:
    prob += lpSum([vars[w][b] for b in TruckStops])<=supply[w], "Sum_of_Products_out_of_Warehouse_%s"%w

# The demand minimum constraints are added to prob for each demand node (TruckStops)
for b in TruckStops:
    prob += lpSum([vars[w][b] for w in Warehouses])>=demand[b], "Sum_of_Products_into_TruckStops%s"%b
                   
# The problem data is written to an .lp file
prob.writeLP("OilDistributionProblem.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen    
print("Total Cost of Transportation = ", value(prob.objective))