from sympy import symbols, Eq, solve, I, pi, sin, cos, symbols, sqrt, re, im


# Tarea 2: Calcular los valores de R, L y C para un circuito RLC en serie

# Definir las variables simbólicas
R, L, C, omega = symbols("R L C omega", real=True, positive=True)

# Frecuencia dada
f = 50  # en Hertz

# Valores eficaces dados
V_R_eficaz = 30  # en Voltios
V_L_eficaz = 70  # en Voltios
V_C_eficaz = 100  # en Voltios
I_eficaz = 10  # en Amperios

# Calcular la velocidad angular omega
omega_val = 2 * pi * f

# Definir las impedancias
Z_R = R
Z_L = I * omega * L
Z_C = 1 / (I * omega * C)

# Ecuaciones basadas en las relaciones de voltaje y corriente
eq1 = Eq(V_R_eficaz, I_eficaz * Z_R)
eq2 = Eq(V_L_eficaz, I_eficaz * abs(Z_L))
eq3 = Eq(V_C_eficaz, I_eficaz * abs(Z_C))

# Resolver las ecuaciones para encontrar R, L y C
soluciones = solve((eq1, eq2, eq3), (R, L, C))

# Calcular la tensión de pico del generador
V_total_eficaz = (V_R_eficaz**2 + (V_L_eficaz - V_C_eficaz) ** 2) ** 0.5
V_in_pico = V_total_eficaz * (2**0.5)

# Calcular los valores de R, L y C utilizando la velocidad angular omega_val
R_val = soluciones[R]
L_val = soluciones[L].subs(omega, omega_val)
C_val = soluciones[C].subs(omega, omega_val)

sol = (round(V_in_pico), R_val, L_val, C_val)
# Format sol to look clean and print with the names of the variables in a Latex format, including the units and the names
print(f"V_{{in}} = {sol[0]} \\, \\text{{V}}")
print(f"R = {sol[1]} \\, \\Omega")
print(f"L = {sol[2]} \\, \\text{{H}}")
print(f"C = {sol[3]} \\, \\text{{F}}")


# Definimos las variables simbólicas para el tiempo y la fase inicial
t, phi = symbols("t phi")

# Calculamos los valores de pico
V_pico = V_in_pico
I_pico = I_eficaz * sqrt(2)

# Expresiones de la tensión y corriente instantáneas
V_in_t = V_pico * cos(omega_val * t + phi)
I_in_t = I_pico * cos(omega_val * t)

# Potencia instantánea
p_t = V_in_t * I_in_t

# Para encontrar la potencia activa y reactiva instantánea, necesitamos el ángulo de fase theta
# Este se encuentra a partir de las reactancias y la resistencia
X_L_val = omega_val * L_val.evalf()
X_C_val = 1 / (omega_val * C_val.evalf())
theta = symbols("theta")

# Potencia activa y reactiva
P = V_total_eficaz * I_eficaz * cos(theta)
Q = V_total_eficaz * I_eficaz * sin(theta)

# Potencia aparente
S = sqrt(P**2 + Q**2)

# Potencia compleja entregada por el generador
S_gen = P + I * Q

# Potencias complejas de cada elemento pasivo
S_R = V_R_eficaz**2 / R_val
S_L = I * V_L_eficaz**2 / X_L_val
S_C = -I * V_C_eficaz**2 / X_C_val

# Balance de potencias
balance_potencias = S_gen - (S_R + S_L + S_C)


# Format the results to look clean and print with the names of the variables in a Latex format, including the units and the names. Include line breaks to make it look better
print(f"V_{{in}}(t) = {V_in_t}")
print(f"I_{{in}}(t) = {I_in_t}")
print(f"p(t) = {p_t}")
print(f"P = {P}")
print(f"Q = {Q}")
print(f"S = {S}")
print(f"S_{{gen}} = {S_gen}")
print(f"S_R = {S_R}")
print(f"S_L = {S_L}")
