import numpy as np

# Costes para cada departamento (D1, D2, D3, D4, D5) y sección (S1,S2,S3,S4)
D1 = np.array([21728, 10000, 150000, 15000])
D2 = np.array([10000, 4629.2, 50000, 20000])
D3 = np.array([25000, 5000, 125925, 20000])
D4 = np.array([3000, 5000, 80000, 6604.6])
D5 = np.array([2000, 5000, 20000, 10000])

# Suma de los costes totales para cada secciónc(S1,S2,S3,S4)
C = D1 + D2 + D3 + D4 + D5

a = np.array(
    [0.75, 0.6, 0.5, 0.4]
)  # Vector de proporciones de los costes totales restantes para cada departamento

b = np.array([C[1], C[0], C[3], C[2]])


# Matriz de coeficientes (A) y vector de constantes (b) para el sistema de ecuaciones corregido
A = np.array(
    [
        [1, -0.4, 0, 0],
        [0, 1, -0.5, 0],
        [0, 0, 1, -0.6],
        [-0.25, 0, 0, 1],
    ]
)

# Resolver el sistema de ecuaciones corregido
x = np.linalg.solve(A, b)
solution = x * a
for index, seccion in enumerate(solution):
    print(f"Coste de la sección S{index+1}: {round(seccion, 2)}")
print(f"Coste total: {np.sum(np.round(solution, 2))}")
