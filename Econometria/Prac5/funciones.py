import statsmodels.api as sm


def backward_elimination(X, y, threshold=0.05):
    """
    Realiza la eliminación progresiva para un modelo lineal.

    Parámetros:
    - X: matriz de predictores.
    - y: vector de la variable de respuesta.
    - threshold: umbral de significancia para mantener una variable en el modelo.

    Retorna:
    - Modelo final después de la eliminación progresiva.
    """

    num_vars = X.shape[1]
    for i in range(0, num_vars):
        model = sm.OLS(y, X).fit()
        max_p_value = max(model.pvalues)
        if max_p_value > threshold:
            remove = (
                model.pvalues.idxmax()
            )  # Identificar variable con el valor p más alto
            X = X.drop(remove, axis=1)  # Eliminar variable
        else:
            break

    return model


# Uso del algoritmo:
# X es tu dataframe de predictores y y es tu serie/vector de respuesta.
# final_model = backward_elimination(X, y)
