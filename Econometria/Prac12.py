"""
1. Clean the data
2. Define the linear model
3. Check multicoliniarity with VIF and correlation matrix (cuantitatve variables)
4. Fit the model
5. Check the parameters, p-values, etc.
6. Check the residuals (white noise)
7. Interpret the results
8. Forecast
* For comparing models, use AIC, BIC, and R^2-adjusted

---
For time series:
- Exponential smoothing (no tendency or seasonality)
- Holt (tendency)
- Holts-Winters (tendency and seasonality)
SARIMA (tendency and seasonality) - Stockastic process (Media 0, Varianza constante, Covarianza constante)
1. Differencing for removing tendency and seasonality: d and D
2. Check autocorrelation and partial autocorrelation: p, q and P, Q, S
3. Choose the best model (AIC, BIC, std. error)
4. Check the residuals (white noise)
6. Forecast and check if the model is good (Average error, not infraestimation or sobreestimation)
"""
