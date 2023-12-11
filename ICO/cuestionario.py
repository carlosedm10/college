# Load the CSV file
import pandas as pd

from utilities import (
    COLUMN_NAMES,
    FRECUENCY_MAPPING,
    IMPORTANCE_MAPPING,
    LIKELIHOOD_MAPPING,
)


file_path = "ICO/TEA IS LIKE A HUG.csv"
data = pd.read_csv(file_path)
################################ DATA PROCESSING ################################

# Renaming the columns
data_cleaned = data.rename(columns=COLUMN_NAMES)

# Changing all string values to have the first character in uppercase
data_cleaned = data_cleaned.applymap(
    lambda x: x.capitalize() if isinstance(x, str) else x
)
data_cleaned = data_cleaned.applymap(
    lambda x: x.strip().capitalize() if isinstance(x, str) else x
)

# Removing rows with any missing values
data_cleaned = data_cleaned.dropna()

# List of columns to apply the importance mapping
columns_to_map = [
    "Importance of Natural Ingredients",
    "Importance of Low Calories",
    "Importance of Brand",
    "Importance of Price",
    "Importance of Flavor",
    "Control Question",
    "Importance of Ready-to-Drink Feature",
    "Importance of Finding Coffee Alternatives",
    "Attractiveness of Healthy Option"
    # Add other relevant columns if necessary
]

# Cuantizing the string values
data_cleaned["Frequency of Cold Beverages"] = data_cleaned[
    "Frequency of Cold Beverages"
].map(FRECUENCY_MAPPING)
data_cleaned["Likelihood of Buying Iced Latte"] = data_cleaned[
    "Likelihood of Buying Iced Latte"
].map(LIKELIHOOD_MAPPING)

print(data_cleaned["Importance of Vegan Alternative"])

for column in columns_to_map:
    print(f"printing column {column}")
    data_cleaned[column] = data_cleaned[column].map(IMPORTANCE_MAPPING)

# Exporting the DataFrame to a CSV file
# export_path = "/Users/carlosedm10/Downloads/prueba.csv"
# data_cleaned.to_csv(export_path, index=False)

# print(f"Data exported successfully to {export_path}")


################################ DATA ANALYSIS ################################
# Number of not ansered questionaries
number_of_responses = len(data)
number_of_valid_responses = len(data_cleaned)
number_of_invalid_responses = number_of_responses - number_of_valid_responses
print(
    f"Number of responses: {number_of_responses}\nNumber of valid responses: {number_of_valid_responses}\nNumber of invalid responses: {number_of_invalid_responses}"
)

# Analyzing preferred tea flavors
preferred_tea_flavors = data_cleaned["Preferred Tea Flavor"].value_counts()

# Analyzing frequency of cold beverage consumption
frequency_of_cold_beverages = data_cleaned["Frequency of Cold Beverages"].value_counts()

# Analyzing likelihood of buying iced latte
likelihood_of_buying_iced_latte = data_cleaned[
    "Likelihood of Buying Iced Latte"
].value_counts()

# Displaying the analysis results
print("Preferred Tea Flavors:\n", preferred_tea_flavors)
print("\nFrequency of Cold Beverage Consumption:\n", frequency_of_cold_beverages)
print("\nLikelihood of Buying Iced Latte:\n", likelihood_of_buying_iced_latte)
