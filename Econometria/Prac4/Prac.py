import xml.etree.ElementTree as ET
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.outliers_influence import variance_inflation_factor


# Parse the XML data
tree = ET.parse("/Users/carlosedm10/projects/college/Econometria/Prac4/MRL028tc.gdt")
root = tree.getroot()

# Extracting variable names from the XML
variable_names = [variable.get("name") for variable in root.findall(".//variable")]

# Extracting all the data from the "obs" tags
all_obs_data = [obs.text.split() for obs in root.findall(".//observations/obs")]

# Convert the extracted data to a DataFrame using the variable names as columns
df = pd.DataFrame(all_obs_data, columns=variable_names)

# Convert to appropriate data types
df = df.apply(pd.to_numeric)

df.head()

# print(df)


# Define dependent variable y and independent variables X
y = df["PARQUE"]
X = df.drop("PARQUE", axis=1)

print(X.columns)

# Add a constant (intercept) to the independent variables
X = sm.add_constant(X)

# Calculate VIF for each independent variable
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print(vif_data)


# Fit the linear regression model
model = sm.OLS(y, X).fit()

# Get the summary of the regression
summary = model.summary()
summary
print(summary)

# Calculating residuals
residuals = model.resid
fitted = model.fittedvalues

# Plotting residuals vs fitted values
plt.figure(figsize=(10, 6))
sns.scatterplot(x=fitted, y=residuals)
plt.axhline(y=0, color="red", linestyle="--")
plt.title("Residuals vs Fitted Values")
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
plt.show()


# Histogram of residuals
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True, bins=20)
plt.title("Histogram of Residuals")
plt.xlabel("Residual")
plt.ylabel("Frequency")
plt.show()

# Q-Q plot for residuals
plt.figure(figsize=(10, 6))
sm.qqplot(residuals, line="45", fit=True)
plt.title("Q-Q Plot of Residuals")
plt.show()

# Plot residuals over time
plt.figure(figsize=(12, 6))
plt.plot(df.index, residuals, marker="o", linestyle="--")
plt.axhline(y=0, color="red", linestyle="-")
plt.title("Residuals over Time")
plt.xlabel("Time")
plt.ylabel("Residual")
plt.show()
