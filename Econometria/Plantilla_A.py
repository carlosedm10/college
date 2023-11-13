"""
1. Escribir el Modelo
2. El modelo es adecuado → Estadistico + prueba + conclusion
3. Determina si la relación entre Y y X no depende del factor (colinealidad)
4. Determina si existen problemas de heterocedasticidad
5. Determine la forma en que causa la desviacion tipica del error (interpreta valores)
"""

from numpy import mean
import pandas as pd
import statsmodels.api as sm
from scipy.stats import f
from utilities import backward_elimination

# Significance level
threshold = 0.05


# Load the CSV file
file_path = "Econometria/MRL016-1.csv"
data = pd.read_csv(file_path)

print(data.head())  # print the first 5 rows to see the data for building the model

########################################## 1. Escribir el Modelo ##########################################

# Creating dummy variables for the 'NPROV' column
dummies = pd.get_dummies(
    data["NPROV"], drop_first=True, dtype=int
)  # drop_first=True to get K-1 dummies out of K categorical levels by removing the first one which is redundant

data = data.drop(["NPROV"], axis=1)  # drop the 'NPROV' column

# --------------------------- Dummy variables ---------------------------#
# print(dummies.head())

data["CASTELLON"] = dummies["CASTELLÓN"]  # interaction variable
data["VALENCIA"] = dummies["VALENCIA"]  # interaction variable

# --------------------------- Adjusted variables ---------------------------#
data["EMPLEOS_AGR_centered"] = data["EMPLEOS_AGR"] - mean(
    data["EMPLEOS_AGR"]
)  # variable independiente

# --------------------------- Interaction variables ---------------------------#

data["EMPLEOS_CASTELLON"] = (
    data["EMPLEOS_AGR"] * dummies["CASTELLÓN"]
)  # interaction variable
data["EMPLEOS_VALENCIA"] = (
    data["EMPLEOS_AGR"] * dummies["VALENCIA"]
)  # interaction variable

# model_data = pd.concat([data, dummies])  # concatenate the data and dummies dataframes

X = data[
    [
        "EMPLEOS_AGR_centered",
        "CASTELLON",
        "VALENCIA",
        "EMPLEOS_CASTELLON",
        "EMPLEOS_VALENCIA",
    ]
]  # variables independientes

X = sm.add_constant(X)  # add a constant to the model
y = data["VAA_AGR"]  # variable dependiente

model = sm.OLS(y, X).fit()  # ordinary least squares model
print(model.summary())  # print the model summary

########################################### 2. El modelo es adecuado ##########################################

print("Deleting the non-significant variables:")
new_model = backward_elimination(X, y, threshold)

print(new_model.summary())

# Degrees of freedom for the model (number of predictors) and residuals (sample size - number of predictors - 1)
df_model = len(X.columns)
df_residuals = len(X) - df_model - 1

f_statistic = new_model.fvalue
f_critical = f.ppf(1 - threshold, df_model, df_residuals)

if f_statistic > f_critical:
    print(f"Fcalc = {f_statistic} > Fcrit = {f_critical}.The model is adequate.")
else:
    print(f"Fcalc = {f_statistic} < Fcrit = {f_critical}.The model is not adequate.")


########################################### * PREDICCIÓN * ##########################################
new_model_params = new_model.params
exog_data = {
    "const": 1,  # Include the constant term
    "EMPLEOS_AGR_centered": [100, 250],  # Example value
    "VALENCIA": [0, 1],  # Example value (1 or 0)
    "EMPLEOS_CASTELLON": [100, 0],  # Example value (EMPLEOS_AGR * CASTELLÓN)
    "EMPLEOS_VALENCIA": [0, 150],  # Example value (EMPLEOS_AGR * VALENCIA)
}  # This is the data given for the prediction
exog_df = pd.DataFrame(exog_data)
predicted_values = new_model.predict(exog=exog_df)

for i in range(len(predicted_values)):
    print(f"The {i+1}º predicted value for {y.name} is: {predicted_values[i]}")
