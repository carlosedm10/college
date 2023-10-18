import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from scipy import stats

# Lectura de datos
df_gretl = pd.read_csv("/mnt/data/MRL028tc.csv", sep=";", skiprows=3)

# Ajuste del modelo inicial con 'PARQUE' como predictor
X_initial = df_gretl["PARQUE"].astype(float)
y_initial = df_gretl["MUERTOS"].astype(float)
X_initial = sm.add_constant(X_initial)
model_initial = sm.OLS(y_initial, X_initial).fit()

# Creación de la variable de interacción
df_gretl["ACCIDENTESxPARQUE"] = df_gretl["ACCIDENTES"].astype(float) * df_gretl[
    "PARQUE"
].astype(float)

# Ajuste del modelo con interacción
X = df_gretl[["PARQUE", "ACCIDENTESxPARQUE"]].astype(float)
X = sm.add_constant(X)
model_interaction = sm.OLS(y, X).fit()

# QQ-plot de los residuos del modelo con interacción
residuals_revised = model_interaction.resid
stats.probplot(residuals_revised, dist="norm", plot=plt)
plt.title("QQ-plot de los residuos del modelo revisado")
plt.show()

# Gráficos de residuos para el modelo con interacción
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 15))
axes[0].scatter(
    model_interaction.fittedvalues, residuals_revised, color="blue", edgecolor="k"
)
axes[0].set_title("Residuos vs Valores Estimados")
axes[1].scatter(
    range(len(residuals_revised)), residuals_revised, color="blue", edgecolor="k"
)
axes[1].set_title("Residuos vs Posición en la tabla")
axes[2].scatter(
    df_gretl["PARQUE"].astype(float), residuals_revised, color="blue", edgecolor="k"
)
axes[2].set_title("Residuos vs PARQUE")
plt.tight_layout()
plt.show()

# Modelo con transformación logarítmica
y_log_revised = np.log(df_gretl["MUERTOS"].astype(float))
model_log_revised = sm.OLS(y_log_revised, X).fit()
