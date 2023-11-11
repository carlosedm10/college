import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm

import numpy as np


def compute_residuals(target_var, predictors, df):
    """Compute residuals for a specific target variable."""
    y = df[target_var]
    X = df[predictors]

    # Add a constant (intercept) to the independent variables
    X = sm.add_constant(X)

    # Fit the model
    model = sm.OLS(y, X).fit()

    # Return residuals
    return model.resid


def eliminate_max_correlated_with_target(df, target):
    """
    Removes the independent variable that has the highest absolute correlation with the target variable.

    Args:
    df (pd.DataFrame): Dataframe with the correlation matrix.
    target (str): Target variable name.

    Returns:
    pd.DataFrame: Updated dataframe with one less independent variable.
    """
    # Compute correlation of all independent variables with the target
    correlations = df.corr()[target].drop(target).abs()

    # Identify the variable with the highest absolute correlation with the target
    column_to_drop = correlations.idxmax()

    # Drop the identified column from the dataframe
    df = df.drop(columns=[column_to_drop])

    return df, column_to_drop


def eliminate_variable_high_pvalue(model, threshold=0.05):
    """
    Identify the variable with the highest p-value greater than the threshold.

    Args:
    model (RegressionResults): Fitted regression model from statsmodels.
    threshold (float, optional): Significance level threshold. Defaults to 0.05.

    Returns:
    str: Name of the variable to be eliminated. Returns None if no variables exceed the threshold.
    """
    # Exclude the constant term when checking p-values
    p_values = model.pvalues.drop("const", errors="ignore")

    # Filter variables with p-values greater than the threshold
    high_p_values = p_values[p_values > threshold]

    # If no variable exceeds the threshold, return None
    if high_p_values.empty:
        return None

    # Identify and return the variable with the highest p-value
    return high_p_values.idxmax()


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
            print("Deleting {} with p-value {}".format(remove, max_p_value))
            X = X.drop(remove, axis=1)  # Eliminar variable
        else:
            break

    return model


# Uso del algoritmo:
# X es tu dataframe de predictores y y es tu serie/vector de respuesta.
# final_model = backward_elimination(X, y)


def forward_selection(X, y):
    """
    Performs forward selection based on residual analysis.

    Parameters:
    - X: DataFrame of predictors.
    - y: Series/vector of response variable.

    Returns:
    - Final model after forward selection.
    """
    remaining_predictors = list(X.columns)
    included_predictors = []
    current_score, best_new_score = float("inf"), float(
        "inf"
    )  # initialized with infinity

    while remaining_predictors and current_score == best_new_score:
        scores_with_predictors = []
        for predictor in remaining_predictors:
            formula = "{} ~ {}".format(
                y.name, " + ".join(included_predictors + [predictor])
            )
            score = sm.OLS.from_formula(formula, data=X.join(y)).fit().ssr
            scores_with_predictors.append((score, predictor))

        scores_with_predictors.sort(reverse=True)
        best_new_score, best_predictor = scores_with_predictors.pop()
        if current_score > best_new_score:
            included_predictors.append(best_predictor)
            remaining_predictors.remove(best_predictor)
            current_score = best_new_score

    formula = "{} ~ {}".format(y.name, " + ".join(included_predictors))
    model = sm.OLS.from_formula(formula, data=X.join(y)).fit()

    return model


# Using the algorithm:
# X is your DataFrame of predictors and y is your Series/vector of response.
# final_model = forward_selection(X, y)


def calculate_max_vif(X):
    """Calculate the maximum VIF for the predictors in X."""
    vif_data = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    return max(vif_data)


def compare_models(X, y):
    # Apply both methods to obtain models
    model_backward = backward_elimination(X, y)
    model_forward = forward_selection(X, y)

    # Compare R^2 adjusted
    if model_backward.rsquared_adj > model_forward.rsquared_adj:
        print("backward_elimination")
        return model_backward
    else:
        print("forward_selection")
        return model_forward


# Using the function:
# X is your DataFrame of predictors and y is your Series/vector of response.
# best_model = compare_models(X, y)
