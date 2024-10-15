import numpy as np
from scipy.optimize import fmin


def eps_r_ef(Er, WH):
    """
    Función para calcular la constante dieléctrica efectiva en una línea microstrip.

    Args:
    Er (numpy array): Constante dieléctrica relativa (puede ser un array).
    WH (numpy array): Relación W/H (ancho sobre altura del substrato).

    Returns:
    numpy array: Constante dieléctrica efectiva.
    """

    if len(Er) != len(WH):
        # Crear una malla de Er y WH si no tienen la misma longitud
        WH, Er = np.meshgrid(WH, Er)

    # Cálculo de la constante dieléctrica efectiva
    E_efec = (Er + 1) / 2 + ((Er - 1) / 2) / np.sqrt(1 + 10 / WH)

    return E_efec


# Función para calcular la longitud de la línea
def calcular_longitud(fc, Epsilon_eff, theta=np.pi / 2):
    L = (3e8 / fc) * (theta / (2 * np.pi * np.sqrt(Epsilon_eff)))
    return L


def ustrip_S(Er, Z0):
    """
    Función para sintetizar líneas microstrip.

    Args:
    Er (numpy array): Constante dieléctrica relativa del sustrato.
    Z0 (numpy array): Impedancia característica deseada (en Ohmios).

    Returns:
    numpy array: Relación W/H (ancho sobre altura del sustrato).
    """

    if len(Z0) != len(Er):
        # Crear una malla de Z0 y Er si no tienen la misma longitud
        Z0, Er = np.meshgrid(Z0, Er)

    # Cálculo de las constantes A y B
    A = (Z0 / 60) * np.sqrt((Er + 1) / 2) + ((Er - 1) / (Er + 1)) * (0.23 + 0.11 / Er)
    B = 60 * np.pi**2 / (Z0 * np.sqrt(Er))

    # Inicializar WH (relación W/H) como un array de ceros del mismo tamaño que Z0
    WH = np.zeros_like(Z0)

    # Encontrar índices donde A <= 1.52
    I1 = np.where(A <= 1.52)
    WH[I1] = (2 / np.pi) * (
        B[I1]
        - 1
        - np.log(-1 + 2 * B[I1])
        + ((Er[I1] - 1) / (2 * Er[I1])) * (0.39 - 0.61 / Er[I1] + np.log(B[I1] - 1))
    )

    # Encontrar índices donde A > 1.52
    I2 = np.where(A > 1.52)
    WH[I2] = 8 * np.exp(A[I2]) / (-2 + np.exp(2 * A[I2]))

    return WH


def ustrip_A(Er, WH):
    """
    Función para analizar líneas microstrip.

    Args:
    Er (numpy array): Constante dieléctrica relativa del sustrato.
    WH (numpy array): Relación ancho/altura de la línea microstrip.

    Returns:
    numpy array: Impedancia característica Z0.
    """

    if len(Er) != len(WH):
        # Crear una malla de WH y Er si no tienen la misma longitud
        WH, Er = np.meshgrid(WH, Er)

    # Inicializar Z0 (Impedancia característica) como un array de ceros del mismo tamaño que WH
    Z0 = np.zeros_like(WH)

    # Calcular la constante dieléctrica efectiva usando la función eps_r_ef
    Er_efec = eps_r_ef(Er, WH)

    # Encontrar índices donde WH <= 1
    I1 = np.where(WH <= 1)
    Z0[I1] = (60 / np.sqrt(Er_efec[I1])) * np.log(8 / WH[I1] + 0.25 * WH[I1])

    # Encontrar índices donde WH > 1
    I2 = np.where(WH > 1)
    Z0[I2] = (120 * np.pi / np.sqrt(Er_efec[I2])) / (
        WH[I2] + 1.393 + 0.667 * np.log(1.444 + WH[I2])
    )

    return Z0


def ustripc_minimize(Y, Z0e, Z0o, Er):
    WH = Y[0]
    SH = Y[1]
    # Aquí debes llamar a la función de análisis 'ustric11' que no está definida en el código original.
    # Asumiendo que 'ustric11' es el análisis para ajustar WH y SH
    # Placeholder return: valor para la minimización (deberías ajustar esto)
    return np.abs(Z0e - Z0o)  # Solo un placeholder, aquí va el análisis real.


def ustripc_S(Z0e, Z0o, Er):
    """
    Función para sintetizar líneas microstrip acopladas.

    Args:
    Z0e (float or numpy array): Impedancia característica del modo par (en Ohmios).
    Z0o (float or numpy array): Impedancia característica del modo impar (en Ohmios).
    Er (float or numpy array): Constante dieléctrica relativa del sustrato.

    Returns:
    tuple: (WH, SH), donde WH es la relación ancho/altura del substrato y SH es la separación entre líneas.
    """

    # Primera estimación de WH para modos par e impar
    WHse = ustrip_S(Er, Z0e / 2)
    WHso = ustrip_S(Er, Z0o / 2)

    # Estimación inicial de WH
    WH = 0.78 * WHso + 0.1 * WHse

    # Cálculo inicial de SH
    SH = np.abs(
        (2 / np.pi)
        * np.arccosh(
            (np.cosh(np.pi * WH / 2) + np.cosh(np.pi * WHse / 2) - 2)
            / (np.cosh(np.pi * WH / 2) - np.cosh(np.pi * WHse / 2))
        )
    )

    # Ejecutar fminsearch para encontrar los valores óptimos de WH y SH
    initial_guess = [WH, SH]
    result = fmin(ustripc_minimize, initial_guess, args=(Z0e, Z0o, Er), disp=False)

    # Actualizar WH y SH con los valores optimizados
    WH = result[0]
    SH = result[1]

    return WH, SH


def ustripc_A(Er, WH, SH):
    """
    Función precisa para calcular las líneas acopladas en microstrip.

    Args:
    Er (float or numpy array): Constante dieléctrica del sustrato.
    WH (float or numpy array): Relación de aspecto de las líneas acopladas (Ancho/Alto).
    SH (float or numpy array): Relación de aspecto de las líneas (Separación/Alto).

    Returns:
    tuple: (Z0e, Z0o, Epsilon_e, Epsilon_o), donde:
        Z0e: Impedancia característica del modo par.
        Z0o: Impedancia característica del modo impar.
        Epsilon_e: Constante dieléctrica efectiva para el modo par.
        Epsilon_o: Constante dieléctrica efectiva para el modo impar.
    """

    # Definir variables intermedias
    u = WH
    g = SH

    # Cálculo de 'a' y 'b'
    a = (
        1
        + np.log((u**4 + (u / 52) ** 2) / (u**4 + 0.432)) / 49
        + np.log(1 + (u / 18.1) ** 3) / 18.7
    )
    b = 0.564 * ((Er - 0.9) / (Er + 3)) ** 0.053

    # Cálculo de otras variables intermedias
    r = 1 + 0.15 * (1 - np.exp(1 - ((Er - 1) ** 2) / 8.2) / (1 + g ** (-6)))
    f01 = 1 - np.exp(
        -0.179 * g**0.15 - 0.328 * (g**r) / np.log(np.exp(1) + (g / 7) ** 2.8)
    )
    q = np.exp(-1.366 - g)
    p = np.exp(-0.745 * g**0.295) / np.cosh(g**0.68)
    f0 = f01 * np.exp(p * np.log(u) + q * np.sin(np.pi * np.log(u) / np.log(10)))

    mu = g * np.exp(-g) + u * (20 + g**2) / (10 + g**2)
    n = (1 / 17.7 + np.exp(-6.424 - 0.76 * np.log(g) - (g / 0.23) ** 5)) * np.log(
        (10 + 68.3 * g**2) / (1 + 32.5 * g**3.093)
    )
    beta = (
        0.2306
        + np.log((g**10) / (1 + (g / 3.73) ** 10)) / 301.8
        + np.log(1 + 0.646 * g**1.175) / 5.3
    )
    teta = 1.729 + 1.175 * np.log(1 + 0.627 / (g + 0.327 * g**2.17))
    m = (
        0.2175
        + (4.113 + (20.36 / g) ** 6) ** (-0.251)
        + np.log((g**10) / (1 + (g / 13.8) ** 10)) / 323
    )
    alfa = 0.5 * np.exp(-g)
    psi = 1 + g / 1.45 + (g**2.09) / 3.95
    phi = 0.8645 * u**0.172

    # Cálculo de phi_e y phi_o
    phi_e = phi / (psi * (alfa * u**m + (1 - alfa) * (u ** (-m))))
    phi_o = phi_e - (teta / psi) * np.exp(beta * (u ** (-n)) * np.log(u))

    # Cálculo de Fo y Fe
    Fo = f0 * (1 + 10 / u) ** (-a * b)
    Fe = (1 + 10 / mu) ** (-a * b)

    # Cálculo de las constantes dieléctricas efectivas
    Epsilon_e = (Er + 1) / 2 + (Er - 1) * Fe / 2
    Epsilon_o = (Er + 1) / 2 + (Er - 1) * Fo / 2

    # Cálculo de las impedancias características
    eta0 = 120 * np.pi / np.sqrt(Er)
    eta0_e = 120 * np.pi / np.sqrt(Epsilon_e)
    eta0_o = 120 * np.pi / np.sqrt(Epsilon_o)

    Z01 = eta0 / (u + 1.98 * u**0.172)
    Z01_e = eta0_e / (u + 1.98 * u**0.172)
    Z01_o = eta0_o / (u + 1.98 * u**0.172)

    Z0e = Z01_e / (1 - Z01_e * phi_e / eta0_e)
    Z0o = Z01_o / (1 - Z01_o * phi_o / eta0_o)

    return Z0e, Z0o, Epsilon_e, Epsilon_o
