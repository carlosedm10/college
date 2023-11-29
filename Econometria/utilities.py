import pandas as pd
import numpy as np
import statsmodels.api as sm

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tsa.stattools import adfuller
from pandas.core.api import DataFrame
from itertools import product
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor


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


def backward_elimination(X, y, threshold):
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
            print("")
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
    model_backward = backward_elimination(X, y, 0.05)
    model_forward = forward_selection(X, y)

    # Compare R^2 adjusted
    if model_backward.rsquared_adj > model_forward.rsquared_adj:
        print("backward_elimination")
        return model_backward
    else:
        print("forward_selection")
        return model_forward


def create_dummies(data: DataFrame) -> DataFrame:
    """
    Create all possible dummy variables for categorical variables.
    The created dummy variables heve the format: {value}
    For example for the column "NPROV" with possible values "ALICANTE", "CASTELLÓN" and "VALENCIA",
    the dummy variables will be "ALICANTE", "CASTELLÓN" and "VALENCIA".
    """
    # Get the categorical variables columns
    categorical_columns = data.select_dtypes(include=["object"]).columns

    # Create dummy variables
    dummies = pd.get_dummies(
        data[categorical_columns],
        prefix="",
        prefix_sep="",
        dtype=int,
    )
    # Concatenate the dummy variables with the original data
    data = pd.concat([data, dummies], axis=1)
    return data


def create_interactions(data: DataFrame) -> DataFrame:
    """
    Create all possible interactions between variables.
    """
    # Iterate over all possible combinations of columns
    for col1, col2 in product(data.columns, data.columns):
        # If the column is categorical, skip it
        categorical_columns = data.select_dtypes(include=["object"]).columns
        if col1 in categorical_columns or col2 in categorical_columns:
            continue

        # If the column is not the same, create the interaction variable
        if col1 != col2:
            data[f"{col1}_{col2}"] = data[col1] * data[col2]

    return data


def make_series_stationary(series, max_diff=3, p_value_threshold=0.05):
    """
    Apply differencing to a time series until it becomes stationary.

    :param series: The original time series.
    :param max_diff: Maximum number of differencing allowed.
    :param p_value_threshold: Threshold for the p-value to consider the series stationary.
    :return: A tuple containing the differenced series and the number of differences applied.
    """

    def adf_test(serie):
        result = adfuller(serie, autolag="AIC")
        return result[1]  # p-value

    # Initial ADF test
    p_value = adf_test(series)
    num_diff = 0

    # Apply differencing until stationary or max_diff reached
    while p_value > p_value_threshold and num_diff < max_diff:
        num_diff += 1
        series = series.diff().dropna()
        p_value = adf_test(series)

    return series, num_diff


# Chequeo de estacionariedad
def check_stationarity(series):
    result = adfuller(series)
    print("Estadístico ADF:", result[0])
    print("Valor p:", result[1])
    print("Valores críticos:")
    for key, value in result[4].items():
        print(f"    {key}: {value}")


def suggest_arima_parameters(acf_values, pacf_values, confidence_interval):
    """
    Suggest ARIMA parameters p and q based on ACF and PACF values.

    :param acf_values: Array of ACF values.
    :param pacf_values: Array of PACF values.
    :param confidence_interval: Confidence interval (e.g., 1.96 for 95%).
    :return: Tuple (p, q) as suggested parameters.
    """
    p = sum(abs(pacf_values) > confidence_interval)
    q = sum(abs(acf_values) > confidence_interval)

    return p, q


def suggest_sarima_parameters(
    acf_values, pacf_values, number_of_diferentiation, s, confidence_interval
):
    """
    Suggest SARIMA parameters (p, d, q, P, D, Q) based on ACF and PACF values.

    :param acf_values: Array of ACF values.
    :param pacf_values: Array of PACF values.
    :param s: Seasonal period.
    :param confidence_interval: Confidence interval (e.g., 1.96 for 95%).
    :return: Tuple (p, d, q, P, D, Q) as suggested parameters.
    """
    # Non-seasonal p and q
    p = sum(abs(pacf_values[: s - 1]) > confidence_interval)
    q = sum(abs(acf_values[: s - 1]) > confidence_interval)

    # Seasonal P and Q
    P = sum(abs(pacf_values[s - 1 :: s]) > confidence_interval)
    Q = sum(abs(acf_values[s - 1 :: s]) > confidence_interval)

    # Assuming D=1 as a common practice for seasonal differencing
    D = number_of_diferentiation

    return p, q, P, D, Q


def generate_all_arima_params(max_value, d, D, S):
    """
    Generate all possible combinations of ARIMA models within the specified parameter ranges.

    :param max_value: Maximum value for the ARIMA p, q, P, Q, and s parameters
    :param d: Value for the ARIMA d parameter
    :param D: Value for the seasonal ARIMA D parameter
    :return: List of tuples representing the ARIMA models
    """
    values = range(max_value + 1)
    params = list(
        product(
            values,
            [d],
            values,
            values,
            [D],
            values,
            [S],
        )
    )
    return params


def fit_arima_model(time_series, spec):
    p, d, q, P, D, Q, s = spec
    try:
        model = ARIMA(time_series, order=(p, d, q), seasonal_order=(P, D, Q, s))
        fitted_model = model.fit()
        return spec, fitted_model.aic, fitted_model.bic
    except Exception as e:
        print(f"Failed to fit model {spec}: {e}")
        return spec, float("inf"), float("inf")  # Return 'inf' to denote failed fitting


def best_arima_models(time_series, arima_specs, num_processes=None):
    with Pool(processes=num_processes) as pool:
        results = pool.starmap(
            fit_arima_model, [(time_series, spec) for spec in arima_specs]
        )

    # Sort the models by AIC and BIC
    sorted_by_aic = sorted(results, key=lambda x: x[1])[:5]
    sorted_by_bic = sorted(results, key=lambda x: x[2])[:5]

    return sorted_by_aic, sorted_by_bic


def best_arima_models(time_series, arima_specs):
    """
    Fit an ARIMA model for each specification in arima_specs to the provided time series.

    :param time_series: Pandas Series representing the time series data
    :param arima_specs: List of tuples with ARIMA specifications (p, d, q, P, D, Q, s)
    :return: List of fitted ARIMA models
    """
    fitted_models_with_criteria = []
    for spec in arima_specs:
        p, d, q, P, D, Q, s = spec
        try:
            model = ARIMA(time_series, order=(p, d, q), seasonal_order=(P, D, Q, s))
            fitted_model = model.fit()
            fitted_models_with_criteria.append(
                (
                    spec,
                    fitted_model.aic,
                    fitted_model.bic,
                )
            )

        except Exception as e:
            print(f"Failed to fit model {spec}: {e}")
            continue

    # Sort the models by AIC and BIC
    sorted_by_aic = sorted(fitted_models_with_criteria, key=lambda x: x[1])[:5]
    sorted_by_bic = sorted(fitted_models_with_criteria, key=lambda x: x[2])[:5]

    return sorted_by_aic, sorted_by_bic


def format_models(models):
    # Formatting the output to match the given picture style
    model_strings = []
    for model in models:
        # Assuming the model tuple structure is (params, AIC, BIC)
        params, aic, bic = model
        model_str = f"({' ,'.join(map(str, params[:-1]))}){params[-1]} - AIC: {aic:.5f} - BIC: {bic:.5f}"
        model_strings.append(model_str)
    return model_strings
