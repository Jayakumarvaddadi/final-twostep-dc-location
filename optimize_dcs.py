import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2
from ortools.linear_solver import pywraplp

stores = pd.read_excel('saavu2.xlsx')
stores.columns = stores.columns.str.lower()

candidates = pd.read_excel('candidate_dcs.xlsx')
candidates.columns = candidates.columns.str.lower()
store_coords = stores[['lat','long']].values
dc_coords = candidates[['lat','long']].values
sales = stores['sales'].values

n = len(store_coords)
m = len(dc_coords)
k = 4

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return 2*R*atan2(sqrt(a), sqrt(1-a))

dist = np.zeros((n,m))
for i in range(n):
    for j in range(m):
        dist[i][j] = haversine(
            store_coords[i][0], store_coords[i][1],
            dc_coords[j][0], dc_coords[j][1]
        )

solver = pywraplp.Solver.CreateSolver('SCIP')

x = {}
y = {}

for i in range(n):
    for j in range(m):
        x[i,j] = solver.BoolVar(f'x_{i}_{j}')

for j in range(m):
    y[j] = solver.BoolVar(f'y_{j}')

for i in range(n):
    solver.Add(sum(x[i,j] for j in range(m)) == 1)

for i in range(n):
    for j in range(m):
        solver.Add(x[i,j] <= y[j])

solver.Add(sum(y[j] for j in range(m)) == k)

solver.Minimize(
    solver.Sum(sales[i]*dist[i][j]*x[i,j] for i in range(n) for j in range(m))
)

solver.Solve()

final_dcs = []
for j in range(m):
    if y[j].solution_value() > 0:
        final_dcs.append(dc_coords[j])

pd.DataFrame(final_dcs, columns=['lat','long']).to_excel(
    'final_dcs.xlsx', index=False
)

assignments = []
for i in range(n):
    for j in range(m):
        if x[i,j].solution_value() > 0:
            assignments.append([i,j,dist[i][j]])

pd.DataFrame(assignments, columns=['store_index','dc_index','distance_km']).to_excel(
    'store_dc_mapping.xlsx', index=False
)

print("Final DCs generated")