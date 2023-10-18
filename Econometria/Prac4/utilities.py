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
