"""
1. Escribir el Modelo por cada nivel de sector
2. El modelo es adecuado → Estadistico + prueba + conclusion
3. Determina si la relación entre Y y X no depende del factor 
4. Determina si existen problemas de heterocedasticidad
5. Determine la forma en que causa la desviacion tipica del error (interpreta valores)
"""

import pandas as pd
import statsmodels.api as sm

from utilities import backward_elimination, compare_models, forward_selection


# Load the CSV file
file_path = "Econometria/MRL016-1.csv"
data = pd.read_csv(file_path)

# Setting up the independent and dependent variables
X = data[["EMPLEOS_AGR"]]  # Predictor
y = data["VAA_AGR"]  # Dependent variable

# Creating dummy variables for the 'NPROV' column
nprov_dummies = pd.get_dummies(data["NPROV"])

# Joining the dummy variables with the original data
data_with_dummies = data.join(nprov_dummies)
X_with_dummies = data_with_dummies.drop(["VAA_AGR", "NPROV"], axis=1)

# Comparing the two models using the compare_models function
best_model = compare_models(X, y)

# Printing the best model method and summary
print(best_model.summary())

model = sm.OLS(y, X).fit()  # ordinary least squares model

print(model.summary())
