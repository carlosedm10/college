# Load the CSV file
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from utilities import add_total_to_legend
from constants import (
    COLUMN_NAMES,
    FRECUENCY_MAPPING,
    FRECUENCY_MAPPING_2,
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
data_cleaned["Iced Latte Tea Consumption Option"] = data_cleaned[
    "Iced Latte Tea Consumption Option"
].map(FRECUENCY_MAPPING_2)


for column in columns_to_map:
    data_cleaned[column] = data_cleaned[column].map(IMPORTANCE_MAPPING)

inconsistency_filter = (
    (data_cleaned["Importance of Vegan Alternative"] > 3)
    & (data_cleaned["Control Question"] < 3)
) | (
    (data_cleaned["Importance of Vegan Alternative"] < 3)
    & (data_cleaned["Control Question"] > 3)
)
# Identify inconsistent responses
inconsistent_responses = data_cleaned[inconsistency_filter]

# Dropping inconsistent responses from the main dataset
data_cleaned = data_cleaned.drop(inconsistent_responses.index)

# Age order for the graphs
age_order = [
    "Menos de 18 años",
    "18-24 años",
    "25-34 años",
    "35-44 años",
    "45-54 años",
    "55 años o más",
]
data_cleaned["Age Range"] = pd.Categorical(
    data_cleaned["Age Range"], categories=age_order, ordered=True
)

# Exporting the DataFrame to a CSV file
# export_path = "/Users/carlosedm10/Downloads/prueba.csv"
# data_cleaned.to_csv(export_path, index=False)

# print(f"Data exported successfully to {export_path}")

################################ DATA ANALYSIS ################################
# Number of not ansered questionaries
number_of_responses = len(data)
number_of_valid_responses = len(data_cleaned) - len(inconsistent_responses)
number_of_invalid_responses = number_of_responses - number_of_valid_responses

print(
    f"Number of responses: {number_of_responses}\nNumber of inconsistent responses: {len(inconsistent_responses)}\nNumber of valid responses: {number_of_valid_responses}\nNumber of invalid responses: {number_of_invalid_responses}\n"
)


# ------------------------------ Consumptions habits ------------------------------
# Analyzing consumption habits based on gender, age, and residence environment

# Setting a consistent color palette for genders across all graphs
palette = {"Femenino": "#1f77b4", "Masculino": "#ff7f0e"}


# Create subplots with three columns
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Frequency of Cold Beverages by Gender
ax0 = sns.countplot(
    x="Frequency of Cold Beverages", data=data_cleaned, color="grey", ax=axes[0]
)
ax0 = sns.countplot(
    x="Frequency of Cold Beverages",
    hue="Gender",
    data=data_cleaned,
    palette=palette,
    ax=axes[0],
)
ax0.set_title("Frequency of Cold Beverages by Gender")
ax0.set_xlabel("Frequency")
ax0.set_ylabel("Count")

# Frequency of Cold Beverages by Age Range
ax1 = sns.countplot(
    x="Frequency of Cold Beverages", data=data_cleaned, color="grey", ax=axes[1]
)
ax1 = sns.countplot(
    x="Frequency of Cold Beverages", hue="Age Range", data=data_cleaned, ax=axes[1]
)
add_total_to_legend(ax1)
ax1.set_title("Frequency of Cold Beverages by Age Range")
ax1.set_xlabel("Frequency")
ax1.set_ylabel("Count")

# Frequency of Cold Beverages by Residence Environment
ax2 = sns.countplot(
    x="Frequency of Cold Beverages", data=data_cleaned, color="grey", ax=axes[2]
)
ax2 = sns.countplot(
    x="Frequency of Cold Beverages",
    hue="Residence Environment",
    data=data_cleaned,
    ax=axes[2],
)
add_total_to_legend(ax2)
ax2.set_title("Frequency of Cold Beverages by Residence Environment")
ax2.set_xlabel("Frequency")
ax2.set_ylabel("Count")

# Adjust spacing between plots
plt.tight_layout()

# Show the plots
plt.show()


# Create subplots with three columns
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Iced Latte Tea Consumption Option by Gender
ax0 = sns.countplot(
    x="Iced Latte Tea Consumption Option", data=data_cleaned, color="grey", ax=axes[0]
)
ax0 = sns.countplot(
    x="Iced Latte Tea Consumption Option",
    hue="Gender",
    data=data_cleaned,
    palette=palette,
    ax=axes[0],
)
add_total_to_legend(ax0)
ax0.set_title("Iced Latte Tea Consumption Option by Gender")
ax0.set_xlabel("Consumption Frequency")
ax0.set_ylabel("Count")
ax0.tick_params(axis="x", rotation=0)

# Importance of Finding Coffee Alternatives by Gender
ax1 = sns.countplot(
    x="Importance of Finding Coffee Alternatives",
    data=data_cleaned,
    color="grey",
    ax=axes[1],
)
ax1 = sns.countplot(
    x="Importance of Finding Coffee Alternatives",
    hue="Gender",
    data=data_cleaned,
    palette=palette,
    ax=axes[1],
)
add_total_to_legend(ax1)
ax1.set_title("Importance of Finding Coffee Alternatives by Gender")
ax1.set_xlabel("Importance Level")
ax1.set_ylabel("Count")
ax1.tick_params(axis="x", rotation=0)

# You can add the third plot here if needed

# Adjust spacing between plots
plt.tight_layout()

# Show the plots
plt.show()

# ----------------------------- Importance of flavor --------------------------------

# Create subplots with two rows and two columns
fig, axes = plt.subplots(2, 2, figsize=(12, 12))

# Importance of Flavor by Gender
ax0 = sns.countplot(
    x="Importance of Flavor", data=data_cleaned, color="grey", ax=axes[0, 0]
)
ax0 = sns.countplot(
    x="Importance of Flavor",
    hue="Gender",
    data=data_cleaned,
    palette=palette,
    ax=axes[0, 0],
)
add_total_to_legend(ax0)
ax0.set_title("Importance of Flavor by Gender")
ax0.set_xlabel("Importance of Flavor")
ax0.set_ylabel("Count")
ax0.tick_params(axis="x", rotation=0)

# Importance of Flavor by Age Range
ax1 = sns.countplot(
    x="Importance of Flavor", data=data_cleaned, color="grey", ax=axes[0, 1]
)
ax1 = sns.countplot(
    x="Importance of Flavor", hue="Age Range", data=data_cleaned, ax=axes[0, 1]
)
add_total_to_legend(ax1)
ax1.set_title("Importance of Flavor by Age Range")
ax1.set_xlabel("Importance of Flavor")
ax1.set_ylabel("Count")
ax1.tick_params(axis="x", rotation=0)

# Preferred Tea Flavor by Gender
ax2 = sns.countplot(
    x="Preferred Tea Flavor", data=data_cleaned, color="grey", ax=axes[1, 0]
)
ax2 = sns.countplot(
    x="Preferred Tea Flavor",
    hue="Gender",
    data=data_cleaned,
    palette=palette,
    ax=axes[1, 0],
)
add_total_to_legend(ax2)
ax2.set_title("Preferred Tea Flavor by Gender")
ax2.set_xlabel("Tea Flavor")
ax2.set_ylabel("Count")
ax2.tick_params(axis="x", rotation=45)

# Preferred Tea Flavor by Age Range
ax3 = sns.countplot(
    x="Preferred Tea Flavor", data=data_cleaned, color="grey", ax=axes[1, 1]
)
ax3 = sns.countplot(
    x="Preferred Tea Flavor", hue="Age Range", data=data_cleaned, ax=axes[1, 1]
)
add_total_to_legend(ax3)
ax3.set_title("Preferred Tea Flavor by Age Range")
ax3.set_xlabel("Tea Flavor")
ax3.set_ylabel("Count")
ax3.tick_params(axis="x", rotation=45)

# Adjust spacing between plots
plt.tight_layout()

# Show the plots
plt.show()

# ----------------------------- Importance of Igredients --------------------------------
# Create a 1x2 grid of plots
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Importance of Natural Ingredients by Gender
ax0 = sns.countplot(
    x="Importance of Natural Ingredients", data=data_cleaned, color="grey", ax=axes[0]
)
ax0 = sns.countplot(
    x="Importance of Natural Ingredients",
    hue="Gender",
    data=data_cleaned,
    palette=palette,
    ax=axes[0],
)
add_total_to_legend(ax0)
ax0.set_title("Importance of Natural Ingredients in Iced Latte by Gender")
ax0.set_xlabel("Importance Level")
ax0.set_ylabel("Count")
ax0.tick_params(axis="x", rotation=0)

# Importance of Natural Ingredients by Age Range
ax1 = sns.countplot(
    x="Importance of Natural Ingredients", data=data_cleaned, color="grey", ax=axes[1]
)
ax1 = sns.countplot(
    x="Importance of Natural Ingredients",
    hue="Age Range",
    data=data_cleaned,
    ax=axes[1],
)
add_total_to_legend(ax1)
ax1.set_title("Importance of Natural Ingredients in Iced Latte by Age Range")
ax1.set_xlabel("Importance Level")
ax1.set_ylabel("Count")
ax1.tick_params(axis="x", rotation=0)

# Adjust spacing between plots
plt.tight_layout()

# Show the plots
plt.show()

# ----------------------------- Importance of Health --------------------------------
# Create a 2x2 grid of plots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Importance of Low Calories by Gender
ax0 = sns.countplot(
    x="Importance of Low Calories", data=data_cleaned, color="grey", ax=axes[0, 0]
)
ax0 = sns.countplot(
    x="Importance of Low Calories",
    hue="Gender",
    data=data_cleaned,
    palette=palette,
    ax=axes[0, 0],
)
add_total_to_legend(ax0)
ax0.set_title("Importance of Low Calories in Iced Latte by Gender")
ax0.set_xlabel("Importance Level")
ax0.set_ylabel("Count")
ax0.tick_params(axis="x", rotation=0)

# Importance of Low Calories by Age Range
ax1 = sns.countplot(
    x="Importance of Low Calories", data=data_cleaned, color="grey", ax=axes[0, 1]
)
ax1 = sns.countplot(
    x="Importance of Low Calories", hue="Age Range", data=data_cleaned, ax=axes[0, 1]
)
add_total_to_legend(ax1)
ax1.set_title("Importance of Low Calories in Iced Latte by Age Range")
ax1.set_xlabel("Importance Level")
ax1.set_ylabel("Count")
ax1.tick_params(axis="x", rotation=0)

# Attractiveness of Healthy Option by Gender
ax2 = sns.countplot(
    x="Attractiveness of Healthy Option", data=data_cleaned, color="grey", ax=axes[1, 0]
)
ax2 = sns.countplot(
    x="Attractiveness of Healthy Option",
    hue="Gender",
    data=data_cleaned,
    palette=palette,
    ax=axes[1, 0],
)
add_total_to_legend(ax2)
ax2.set_title("Attractiveness of Healthy Option in Iced Latte by Gender")
ax2.set_xlabel("Attractiveness Level")
ax2.set_ylabel("Count")
ax2.tick_params(axis="x", rotation=0)

# Attractiveness of Healthy Option by Age Range
ax3 = sns.countplot(
    x="Attractiveness of Healthy Option", data=data_cleaned, color="grey", ax=axes[1, 1]
)
ax3 = sns.countplot(
    x="Attractiveness of Healthy Option",
    hue="Age Range",
    data=data_cleaned,
    ax=axes[1, 1],
)
add_total_to_legend(ax3)
ax3.set_title("Attractiveness of Healthy Option in Iced Latte by Age Range")
ax3.set_xlabel("Attractiveness Level")
ax3.set_ylabel("Count")
ax3.tick_params(axis="x", rotation=0)

# Adjust spacing between plots
plt.tight_layout()

# Show the plots
plt.show()
# ----------------------------- Importance of Veganism --------------------------------
# Create a 1x2 grid of plots
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Importance of Vegan Alternative by Gender
ax0 = sns.countplot(
    x="Importance of Vegan Alternative", data=data_cleaned, color="grey", ax=axes[0]
)
ax0 = sns.countplot(
    x="Importance of Vegan Alternative",
    hue="Gender",
    data=data_cleaned,
    palette=palette,
    ax=axes[0],
)
add_total_to_legend(ax0)
ax0.set_title("Importance of Vegan Alternative in Beverages by Gender")
ax0.set_xlabel("Importance Level")
ax0.set_ylabel("Count")
ax0.tick_params(axis="x", rotation=0)

# Importance of Vegan Alternative by Age Range
ax1 = sns.countplot(
    x="Importance of Vegan Alternative", data=data_cleaned, color="grey", ax=axes[1]
)
ax1 = sns.countplot(
    x="Importance of Vegan Alternative", hue="Age Range", data=data_cleaned, ax=axes[1]
)
add_total_to_legend(ax1)
ax1.set_title("Importance of Vegan Alternative in Beverages by Age Range")
ax1.set_xlabel("Importance Level")
ax1.set_ylabel("Count")
ax1.tick_params(axis="x", rotation=0)

# Adjust spacing between plots
plt.tight_layout()

# Show the plots
plt.show()

# ----------------------------- Chanel of Sales --------------------------------
# Create a 2x2 grid of plots
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Likelihood of Buying Iced Latte by Gender
ax0 = sns.countplot(
    x="Likelihood of Buying Iced Latte", data=data_cleaned, color="grey", ax=axes[0]
)
ax0 = sns.countplot(
    x="Likelihood of Buying Iced Latte",
    hue="Residence Environment",
    data=data_cleaned,
    ax=axes[0],
)
add_total_to_legend(ax0)
ax0.set_title("Likelihood of Buying Iced Latte in Supermarkets by Importance Level")
ax0.set_xlabel("Importance Level")
ax0.set_ylabel("Count")
ax0.tick_params(axis="x", rotation=0)

# Preferred Purchase Location by Age Range
ax1 = sns.countplot(
    x="Preferred Purchase Location", data=data_cleaned, color="grey", ax=axes[1]
)
ax1 = sns.countplot(
    x="Preferred Purchase Location",
    hue="Residence Environment",
    data=data_cleaned,
    ax=axes[1],
)
add_total_to_legend(ax1)
ax1.set_title("Preferred Purchase Location by Residence Environment")
ax1.set_xlabel("Place")
ax1.set_ylabel("Count")
ax1.tick_params(axis="x", rotation=0)

# Adjust spacing between plots
plt.tight_layout()

# Show the plots
plt.show()

# ----------------------------- Brand Importance and Pricing --------------------------------
# Create a 2x2 grid of plots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Importance of Brand by Current Situation
ax0 = sns.countplot(
    x="Importance of Brand", data=data_cleaned, color="grey", ax=axes[0, 0]
)
ax0 = sns.countplot(
    x="Importance of Brand",
    hue="Current Situation",  # Replace with the appropriate column name
    data=data_cleaned,
    ax=axes[0, 0],
)
add_total_to_legend(ax0)
ax0.set_title("Importance of Brand by Current Situation")
ax0.set_xlabel("Importance Level")
ax0.set_ylabel("Count")
ax0.tick_params(axis="x", rotation=0)

# Importance of Price by Current Situation
ax1 = sns.countplot(
    x="Importance of Price", data=data_cleaned, color="grey", ax=axes[0, 1]
)
ax1 = sns.countplot(
    x="Importance of Price",
    hue="Current Situation",  # Replace with the appropriate column name
    data=data_cleaned,
    ax=axes[0, 1],
)
add_total_to_legend(ax1)
ax1.set_title("Importance of Price by Current Situation")
ax1.set_xlabel("Importance Level")
ax1.set_ylabel("Count")
ax1.tick_params(axis="x", rotation=0)

# Too Expensive Price Range by Current Situation
ax2 = sns.countplot(
    x="Too Expensive Price Range", data=data_cleaned, color="grey", ax=axes[1, 0]
)
ax2 = sns.countplot(
    x="Too Expensive Price Range",
    hue="Current Situation",  # Replace with the appropriate column name
    data=data_cleaned,
    ax=axes[1, 0],
)
add_total_to_legend(ax2)
ax2.set_title("Too Expensive Price Range by Current Situation")
ax2.set_xlabel("Price Range")
ax2.set_ylabel("Count")
ax2.tick_params(axis="x", rotation=45)

# Too Cheap Price Range by Current Situation
ax3 = sns.countplot(
    x="Too Cheap Price Range", data=data_cleaned, color="grey", ax=axes[1, 1]
)
ax3 = sns.countplot(
    x="Too Cheap Price Range",
    hue="Current Situation",  # Replace with the appropriate column name
    data=data_cleaned,
    ax=axes[1, 1],
)
add_total_to_legend(ax3)
ax3.set_title("Too Cheap Price Range by Current Situation")
ax3.set_xlabel("Price Range")
ax3.set_ylabel("Count")
ax3.tick_params(axis="x", rotation=45)

# Adjust spacing between plots
plt.tight_layout()

# Show the plots
plt.show()

# ----------------------------- Idea Validation --------------------------------
# Create a 2x2 grid of plots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Specialness of Product Idea by Gender
ax0 = sns.countplot(
    x="Specialness of Product Idea", data=data_cleaned, color="grey", ax=axes[0, 0]
)
ax0 = sns.countplot(
    x="Specialness of Product Idea",
    hue="Gender",  # Replace with the actual column name for gender
    data=data_cleaned,
    ax=axes[0, 0],
)
add_total_to_legend(ax0)
ax0.set_title("Specialness of Product Idea by Gender")
ax0.set_xlabel("Specialness Level")
ax0.set_ylabel("Count")
ax0.tick_params(axis="x", rotation=0)

# Specialness of Product Idea by Age
ax1 = sns.countplot(
    x="Specialness of Product Idea", data=data_cleaned, color="grey", ax=axes[0, 1]
)
ax1 = sns.countplot(
    x="Specialness of Product Idea",
    hue="Age Range",  # Replace with the actual column name for age range
    data=data_cleaned,
    ax=axes[0, 1],
)
add_total_to_legend(ax1)
ax1.set_title("Specialness of Product Idea by Age Range")
ax1.set_xlabel("Specialness Level")
ax1.set_ylabel("Count")
ax1.tick_params(axis="x", rotation=0)

# Importance of Ready-to-Drink Feature by Gender
ax2 = sns.countplot(
    x="Importance of Ready-to-Drink Feature",
    data=data_cleaned,
    color="grey",
    ax=axes[1, 0],
)
ax2 = sns.countplot(
    x="Importance of Ready-to-Drink Feature",
    hue="Gender",  # Replace with the actual column name for gender
    data=data_cleaned,
    ax=axes[1, 0],
)
add_total_to_legend(ax2)
ax2.set_title("Importance of Ready-to-Drink Feature by Gender")
ax2.set_xlabel("Importance Level")
ax2.set_ylabel("Count")
ax2.tick_params(axis="x", rotation=0)

# Importance of Ready-to-Drink Feature by Age
ax3 = sns.countplot(
    x="Importance of Ready-to-Drink Feature",
    data=data_cleaned,
    color="grey",
    ax=axes[1, 1],
)
ax3 = sns.countplot(
    x="Importance of Ready-to-Drink Feature",
    hue="Age Range",  # Replace with the actual column name for age range
    data=data_cleaned,
    ax=axes[1, 1],
)
add_total_to_legend(ax3)
ax3.set_title("Importance of Ready-to-Drink Feature by Age Range")
ax3.set_xlabel("Importance Level")
ax3.set_ylabel("Count")
ax3.tick_params(axis="x", rotation=0)

# Adjust spacing between plots
plt.tight_layout()

# Show the plots
plt.show()
