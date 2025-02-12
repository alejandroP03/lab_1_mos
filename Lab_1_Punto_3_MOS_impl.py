import matplotlib.pyplot as plt
from pyomo.environ import *

# =====================
# Datos del Problema
# =====================
recursos = [1, 2, 3, 4, 5]  # 1: Alimentos, 2: Medicinas, 3: Equipos Médicos, 4: Agua, 5: Mantas
aviones = [1, 2, 3]

# Parámetros
valor = {1: 50, 2: 100, 3: 120, 4: 60, 5: 40}       # Valor de cada recurso
peso = {1: 15, 2: 5, 3: 20, 4: 18, 5: 10}           # Peso (TON) de cada recurso
volumen = {1: 8, 2: 2, 3: 10, 4: 12, 5: 6}          # Volumen (m³) de cada recurso

capacidad_peso = {1: 30, 2: 40, 3: 50}              # Capacidad de peso por avión
capacidad_volumen = {1: 25, 2: 30, 3: 35}           # Capacidad de volumen por avión

# =====================
# Modelo en Pyomo
# =====================
model = ConcreteModel()

# Conjuntos
model.R = Set(initialize=recursos)
model.A = Set(initialize=aviones)

# Variables de decisión (binarias)
model.X = Var(model.R, model.A, domain=Binary)

# Función Objetivo: Maximizar el valor total de los recursos transportados
def objective_rule(model):
    return sum(valor[i] * model.X[i, j] for i in model.R for j in model.A)
model.obj = Objective(rule=objective_rule, sense=maximize)

# Restricciones
# 1. Capacidad de Peso
model.peso_constraint = ConstraintList()
for j in model.A:
    model.peso_constraint.add(
        sum(peso[i] * model.X[i, j] for i in model.R) <= capacidad_peso[j]
    )

# 2. Capacidad de Volumen
model.volumen_constraint = ConstraintList()
for j in model.A:
    model.volumen_constraint.add(
        sum(volumen[i] * model.X[i, j] for i in model.R) <= capacidad_volumen[j]
    )

# 3. Asignación Única (cada recurso solo en un avión)
model.asignacion_unica = ConstraintList()
for i in model.R:
    model.asignacion_unica.add(
        sum(model.X[i, j] for j in model.A) <= 1
    )

# 4. Medicinas NO en Avión 1
model.medicina_restriccion = Constraint(expr=model.X[2, 1] == 0)

# 5. Equipos Médicos y Agua NO en el mismo avión
model.compatibilidad_restriccion = ConstraintList()
for j in model.A:
    model.compatibilidad_restriccion.add(
        model.X[3, j] + model.X[4, j] <= 1
    )

# =====================
# Solución
# =====================
solver = SolverFactory('glpk')
solver.solve(model)

# =====================
# Resultados
# =====================
print("--- Asignación de Recursos ---")
print("Valor total transportado:", model.obj())
for i in model.R:
    for j in model.A:
        if model.X[i, j].value == 1:
            print(f"Recurso {i} asignado al Avión {j}")

# =====================
# Visualización
# =====================
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# 1. Scatter Plot de Asignación
asignaciones = [(i, j) for i in model.R for j in model.A if model.X[i, j].value == 1]
for i, j in asignaciones:
    axs[0].scatter(j, i, color='green')
axs[0].set_title('Asignación de Recursos a Aviones')
axs[0].set_xlabel('Aviones')
axs[0].set_ylabel('Recursos')
axs[0].set_xticks(aviones)
axs[0].set_yticks(recursos)
axs[0].grid(True)

# 2. Gráfico de Barras: Valor Total Transportado por Avión
valor_por_avion = [sum(valor[i] * model.X[i, j].value for i in model.R) for j in model.A]
axs[1].bar(aviones, valor_por_avion, color='skyblue')
axs[1].set_xlabel('Aviones')
axs[1].set_ylabel('Valor Transportado')
axs[1].set_title('Valor Total Transportado por Avión')

plt.tight_layout()
plt.show()