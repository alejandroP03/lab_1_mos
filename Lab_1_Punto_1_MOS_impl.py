import matplotlib.pyplot as plt
from pyomo.environ import *

# Punto 1
NUM_TASKS = 11
MAX_POINTS = 52

s_i = [5, 3, 13, 1, 21, 2, 2, 5, 8, 13, 21]

priorities = ["Máxima", "Media alta", "Alta", "Media baja", "Mínima", "Media", "Alta", "Alta", "Baja", "Máxima", "Alta"]
prior_val = {
    "Mínima": 1,
    "Baja": 2,
    "Media baja": 3,
    "Media": 4,
    "Media alta": 5,
    "Alta": 6,
    "Máxima": 7
}

p_i = [prior_val[p] for p in priorities]

# Parte A
model = ConcreteModel()
model.i = RangeSet(NUM_TASKS)
model.x = Var(model.i, domain=Binary)
model.obj = Objective(expr=sum(p_i[i-1]*model.x[i] for i in model.i), sense=maximize)
model.rest_num_points = ConstraintList()
model.rest_num_points.add(sum(model.x[i]  * s_i[i-1] for i in model.i) <= MAX_POINTS)

solver = SolverFactory('glpk')
solver.solve(model)

for i in model.i:
    print(f"Task {i} is {model.x[i].value}")

fig, ax1 = plt.subplots()

ax1.bar(range(1, NUM_TASKS+1), [model.x[i].value for i in model.i], label="Assigned")
ax1.set_xlabel('Task')
ax1.set_ylabel('Assigned')
ax1.set_yticks([0, 1])
ax1.tick_params(axis='y')

ax2 = ax1.twinx()
ax2.plot(range(1, NUM_TASKS+1), [p_i[i-1] for i in model.i], 'r', label="Priority")
ax2.set_ylabel('Priority')
ax2.set_yticks(range(1, 8))
ax2.tick_params(axis='y')

fig.tight_layout()
plt.show()

# Parte B
NUM_DEVS = 4
MAX_DEV_POINTS = 13

model = ConcreteModel()
model.i = RangeSet(NUM_TASKS)
model.j = RangeSet(NUM_DEVS)
model.x = Var(model.i, model.j, domain=Binary)
model.obj = Objective(expr=sum(p_i[i-1]*model.x[i,j] for i in model.i for j in model.j), sense=maximize)
model.rest_num_points = ConstraintList()
model.rest_task_per_dev = ConstraintList()

for j in model.j:
    model.rest_num_points.add(sum(model.x[i,j] * s_i[i-1] for i in model.i) <= MAX_DEV_POINTS)

for i in model.i:
    model.rest_task_per_dev.add(sum(model.x[i,j] for j in model.j) <= 1)

solver = SolverFactory('glpk')
solver.solve(model)

for j in model.j:
    for i in model.i:
        if model.x[i,j].value == 1:
            print(f"Task {i} is assigned to developer {j}")


fig, ax1 = plt.subplots()

ax1.scatter([i for i in model.i for j in model.j if model.x[i,j].value == 1], [j for j in model.j for i in model.i if model.x[i,j].value == 1], label="Assigned")

ax1.set_xlabel('Task')
ax1.set_ylabel('Assigned')

ax1.set_yticks(range(1, NUM_DEVS+1))
ax1.set_xticks(range(1, NUM_TASKS+1))


plt.show()