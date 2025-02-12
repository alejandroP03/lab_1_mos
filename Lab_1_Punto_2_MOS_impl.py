from pyomo.environ import *
import matplotlib.pyplot as plt
import numpy as np

# Datos
trabajadores = [1, 2, 3]
trabajos = [1, 2, 3, 4, 5]

# Ganancia por trabajo
g = {1: 50, 2: 60, 3: 40, 4: 70, 5: 30}
# Horas requeridas por trabajo
h = {1: 4, 2: 5, 3: 3, 4: 6, 5: 2}
# Horas disponibles por trabajador
C = {1: 8, 2: 10, 3: 6}

model_A = ConcreteModel()

# Conjuntos
model_A.W = Set(initialize=trabajadores)
model_A.T = Set(initialize=trabajos)

# Variable de decisión
model_A.x = Var(model_A.W, model_A.T, domain=Binary)

# Función objetivo
def objective_rule_A(model):
    return sum(g[k] * model.x[i, k] for i in model.W for k in model.T)

model_A.obj = Objective(rule=objective_rule_A, sense=maximize)

# Restricción: Asignación única
model_A.assignment_constraint = ConstraintList()
for k in model_A.T:
    model_A.assignment_constraint.add(sum(model_A.x[i, k] for i in model_A.W) <= 1)

# Restricción de disponibilidad horaria
for i in model_A.W:
    model_A.assignment_constraint.add(
        sum(h[k] * model_A.x[i, k] for k in model_A.T) <= C[i]
    )

# Solución del modelo A
solver = SolverFactory('glpk', executable='/usr/bin/glpsol')
solver.solve(model_A)

tiempo_total_utilizado_A = sum(h[k] * model_A.x[i, k].value for i in model_A.W for k in model_A.T)

# Resultados Parte A
print("Ganancia total obtenida:", model_A.obj())
print(f"\nTiempo total utilizado: {tiempo_total_utilizado_A} horas")
for i in model_A.W:
    for k in model_A.T:
        if model_A.x[i, k].value == 1:
            print(f"Trabajador {i} realiza el Trabajo {k} (Horas: {h[k]})")

fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Gráfico de Asignación (Parte A)
assignments_A = [(i, k) for i in model_A.W for k in model_A.T if model_A.x[i, k].value == 1]
for i, k in assignments_A:
    axs[0].scatter(k, i, color='green')
axs[0].set_title('Parte A: Asignación Básica')
axs[0].set_xlabel('Trabajos')
axs[0].set_ylabel('Trabajadores')
axs[0].set_xticks(trabajos)
axs[0].set_yticks(trabajadores)
axs[0].grid(True)

# Gráfico de Barras: Horas utilizadas por trabajador (Parte A)
horas_por_trabajador = [sum(h[k] * model_A.x[i, k].value for k in model_A.T) for i in model_A.W]
axs[1].bar(trabajadores, horas_por_trabajador, color='skyblue')
axs[1].set_xlabel("Trabajadores")
axs[1].set_ylabel("Horas Utilizadas")
axs[1].set_title("Horas Totales Utilizadas por Trabajador (Parte A)")

plt.tight_layout()
plt.show()

#Punto B
model_B = ConcreteModel()

# Conjuntos
model_B.W = Set(initialize=trabajadores)
model_B.T = Set(initialize=trabajos)

# Variables de decisión
model_B.x = Var(model_B.W, model_B.T, domain=Binary)

# Función objetivo: maximizar la ganancia total
def objective_rule_B(model):
    return sum(g[k] * model.x[i, k] for i in model.W for k in model.T)
model_B.obj = Objective(rule=objective_rule_B, sense=maximize)

# Restricción de asignación única
model_B.assignment_constraint = ConstraintList()
for k in model_B.T:
    model_B.assignment_constraint.add(
        sum(model_B.x[i, k] for i in model_B.W) <= 1
    )

# Restricción de disponibilidad horaria
for i in model_B.W:
    model_B.assignment_constraint.add(
        sum(h[k] * model_B.x[i, k] for k in model_B.T) <= C[i]
    )

# Restricciones adicionales
# Solo el trabajador 1 puede realizar el Trabajo 1
for i in model_B.W:
    if i != 1:
        model_B.assignment_constraint.add(model_B.x[i, 1] == 0)

# El Trabajo 3 no puede ser realizado por el trabajador 2
model_B.assignment_constraint.add(model_B.x[2, 3] == 0)

# Solución del modelo B
solver.solve(model_B)

# Resultados Parte B
print("\n--- Parte B: Asignación con Restricciones Adicionales ---")
print("Ganancia total obtenida:", model_B.obj())
for i in model_B.W:
    for k in model_B.T:
        if model_B.x[i, k].value == 1:
            print(f"Trabajador {i} realiza el Trabajo {k} (Horas: {h[k]})")

figb, axsb = plt.subplots(1, 2, figsize=(12, 5))

# Parte B - Scatter
assignments_B = [(i, k) for i in model_B.W for k in model_B.T if model_B.x[i, k].value == 1]
for i, k in assignments_B:
    axsb[0].scatter(k, i, color='blue')
axsb[0].set_title('Parte B: Asignación con Restricciones')
axsb[0].set_xlabel('Trabajos')
axsb[0].set_ylabel('Trabajadores')
axsb[0].set_xticks(trabajos)
axsb[0].set_yticks(trabajadores)
axsb[0].grid(True)

# Parte B - Barras
horas_por_trabajador_B = [sum(h[k] * model_B.x[i, k].value for k in model_B.T) for i in model_B.W]
axsb[1].bar(trabajadores, horas_por_trabajador_B, color='lightcoral')
axsb[1].set_xlabel("Trabajadores")
axsb[1].set_ylabel("Horas Utilizadas")
axsb[1].set_title("Horas Totales Utilizadas por Trabajador (Parte B)")

plt.tight_layout()
plt.show()