# Load the CSV file
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from utilities import add_total_to_legend, generate_statistics_for_dataset
from constants import (
    COLUMN_NAMES,
    FRECUENCY_MAPPING,
    FRECUENCY_MAPPING_2,
    IMPORTANCE_MAPPING,
    LIKELIHOOD_MAPPING,
)
from scipy.stats import chi2_contingency

file_path = "ICO/TEA IS LIKE A HUG.csv"
save_path = "/Users/carlosedm10/Downloads/"
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

# Top price order for the graphs
top_price_order = [
    "Hasta 0,8€",
    "De 0,8 hasta 1€",
    "De 1 a 1,5€",
    "Más de 1,5€",
]
data_cleaned["Too Expensive Price Range"] = pd.Categorical(
    data_cleaned["Too Expensive Price Range"], categories=top_price_order, ordered=True
)

# Low price order for the graphs
low_price_order = [
    "Hasta 0,5€",
    "De 0,5 hasta 1€",
    "De 1 a 1,5€",
    "Ninguna de las anteriores",
]
data_cleaned["Too Cheap Price Range"] = pd.Categorical(
    data_cleaned["Too Cheap Price Range"], categories=low_price_order, ordered=True
)

# Exporting the DataFrame to a CSV file
# export_path = "/Users/carlosedm10/Downloads/prueba.csv"
# data_cleaned.to_csv(export_path, index=False)

# print(f"Data exported successfully to {export_path}")

################################ DATA ANALYSIS ################################

# ------------------------------ General Statistics ------------------------------
cross_val_attributes = [
    "Age Range",
    "Gender",
    "Current Situation",
    "Residence Environment",
]

generate_statistics_for_dataset(
    data_cleaned, cross_val_attributes=cross_val_attributes, threshold=0.1
)


# Number of not ansered questionaries
number_of_responses = len(data)
number_of_valid_responses = len(data_cleaned) - len(inconsistent_responses)
number_of_inconsistent_responses = len(inconsistent_responses)
number_of_invalid_clients = (
    number_of_responses - number_of_valid_responses - number_of_inconsistent_responses
)

print(
    f"Number of responses: {number_of_responses}\nNumber of valid responses: {number_of_valid_responses}\nNumber of inconsistent responses: {number_of_inconsistent_responses}\nNumber of invalid responses: {number_of_invalid_clients}\n"
)
labels = ["Valid Responses", "Inconsistent Responses", "Invalid Clients"]
sizes = [
    number_of_valid_responses,
    number_of_inconsistent_responses,
    number_of_invalid_clients,
]

# Create a pie chart
plt.figure(figsize=(8, 8))
plt.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    startangle=140,
)

# Add a title
plt.title(f"Statistics for {number_of_responses} Responses")

# Display the plot
plt.axis("equal")  # Ensure a circular pie chart
# plt.show()
# Display the plot
plt.axis("equal")  # Ensure a circular pie chart
plt.savefig(f"{save_path}Responses pie.png")

# Select columns for pie charts
columns_for_pie_charts = ["Gender", "Age Range", "Residence Environment"]

# Iterate through the selected columns and create pie charts
for column in columns_for_pie_charts:
    # Calculate value counts for the column
    value_counts = data_cleaned[column].value_counts()

    # Create a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(value_counts, labels=value_counts.index, autopct="%1.1f%%", startangle=140)

    # Add a title based on the column name
    plt.title(f"{column} Distribution")

    # Display the plot
    plt.axis("equal")  # Ensure a circular pie chart
    plt.savefig(f"{save_path}{column} pie.png")
    # plt.show()

# ------------------------------ Consumptions habits ------------------------------

# Analyzing consumption habits based on gender, age

# Setting a consistent color palette for genders across all graphs
palette = {"Femenino": "#1f77b4", "Masculino": "#ff7f0e"}


# Create subplots with three columns
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Frequency of Cold Beverages"], data_cleaned["Gender"]
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Frequency of Cold Beverages by Gender
ax0 = sns.countplot(
    x="Frequency of Cold Beverages", data=data_cleaned, color="grey", ax=axes[0, 0]
)
ax0 = sns.countplot(
    x="Frequency of Cold Beverages",
    hue="Gender",
    data=data_cleaned,
    palette=palette,
    ax=axes[0, 0],
)
add_total_to_legend(ax0)
ax0.set_title(f"Frequency of Cold Beverages by Gender (p-value: {p_value:.2f})")
ax0.set_xlabel("Frequency")
ax0.set_ylabel("Count")

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Frequency of Cold Beverages"], data_cleaned["Age Range"]
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Frequency of Cold Beverages by Age Range
ax1 = sns.countplot(
    x="Frequency of Cold Beverages", data=data_cleaned, color="grey", ax=axes[1, 0]
)
ax1 = sns.countplot(
    x="Frequency of Cold Beverages", hue="Age Range", data=data_cleaned, ax=axes[1, 0]
)
add_total_to_legend(ax1)
ax1.set_title(f"Frequency of Cold Beverages by Age Range (p-value: {p_value:.2f})")
ax1.set_xlabel("Frequency")
ax1.set_ylabel("Count")

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Importance of Finding Coffee Alternatives"], data_cleaned["Gender"]
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Importance of Finding Coffee Alternatives by Gender
ax2 = sns.countplot(
    x="Importance of Finding Coffee Alternatives",
    data=data_cleaned,
    color="grey",
    ax=axes[0, 1],
)
ax2 = sns.countplot(
    x="Importance of Finding Coffee Alternatives",
    hue="Gender",
    data=data_cleaned,
    palette=palette,
    ax=axes[0, 1],
)
add_total_to_legend(ax2)
ax2.set_title(
    f"Importance of Finding Coffee Alternatives by Gender (p-value: {p_value:.2f})"
)
ax2.set_xlabel("Importance Level")
ax2.set_ylabel("Count")
ax2.tick_params(axis="x", rotation=0)

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Importance of Finding Coffee Alternatives"], data_cleaned["Age Range"]
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Importance of Finding Coffee Alternatives by Gender
ax3 = sns.countplot(
    x="Importance of Finding Coffee Alternatives",
    data=data_cleaned,
    color="grey",
    ax=axes[1, 1],
)
ax3 = sns.countplot(
    x="Importance of Finding Coffee Alternatives",
    hue="Age Range",
    data=data_cleaned,
    ax=axes[1, 1],
)
add_total_to_legend(ax3)
ax3.set_title(
    f"Importance of Finding Coffee Alternatives by Age Range (p-value: {p_value:.2f})"
)
ax3.set_xlabel("Importance Level")
ax3.set_ylabel("Count")
ax3.tick_params(axis="x", rotation=0)

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Attractiveness of Healthy Option"], data_cleaned["Gender"]
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Attractiveness of Healthy Option by Gender
ax4 = sns.countplot(
    x="Attractiveness of Healthy Option", data=data_cleaned, color="grey", ax=axes[0, 2]
)
ax4 = sns.countplot(
    x="Attractiveness of Healthy Option",
    hue="Gender",
    data=data_cleaned,
    palette=palette,
    ax=axes[0, 2],
)
add_total_to_legend(ax4)
ax4.set_title(
    f"Attractiveness of Healthy Option in Iced Latte by Gender (p-value: {p_value:.2f})"
)
ax4.set_xlabel("Attractiveness Level")
ax4.set_ylabel("Count")
ax4.tick_params(axis="x", rotation=0)

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Attractiveness of Healthy Option"], data_cleaned["Age Range"]
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Attractiveness of Healthy Option by Age Range
ax5 = sns.countplot(
    x="Attractiveness of Healthy Option", data=data_cleaned, color="grey", ax=axes[1, 2]
)
ax5 = sns.countplot(
    x="Attractiveness of Healthy Option",
    hue="Age Range",
    data=data_cleaned,
    ax=axes[1, 2],
)
add_total_to_legend(ax5)
ax5.set_title(
    f"Attractiveness of Healthy Option in Iced Latte by Age Range (p-value: {p_value:.2f})"
)
ax5.set_xlabel("Attractiveness Level")
ax5.set_ylabel("Count")
ax5.tick_params(axis="x", rotation=0)


# Adjust spacing between plots
plt.tight_layout()

# Show the plots
# plt.show()

tittle = "Consumption Habits"
plt.savefig(f"{save_path}{tittle} plot.png")
# ------------------------------ Product Characteristics ------------------------------


# Create subplots with two rows and two columns
fig, axes = plt.subplots(2, 2, figsize=(18, 12))

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Importance of Flavor"], data_cleaned["Gender"]
)
_, p_value, _, _ = chi2_contingency(contingency_table)
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
ax0.set_title(f"Importance of Flavor by Gender (p-value: {p_value:.2f})")
ax0.set_xlabel("Importance of Flavor")
ax0.set_ylabel("Count")
ax0.tick_params(axis="x", rotation=0)

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Importance of Natural Ingredients"], data_cleaned["Gender"]
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Importance of Natural Ingredients by Gender
ax1 = sns.countplot(
    x="Importance of Natural Ingredients",
    data=data_cleaned,
    color="grey",
    ax=axes[0, 1],
)
ax1 = sns.countplot(
    x="Importance of Natural Ingredients",
    hue="Gender",
    data=data_cleaned,
    palette=palette,
    ax=axes[0, 1],
)
add_total_to_legend(ax1)
ax1.set_title(f"Importance of Natural Ingredients by Gender (p-value: {p_value:.2f})")
ax1.set_xlabel("Importance Level")
ax1.set_ylabel("Count")
ax1.tick_params(axis="x", rotation=0)

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Importance of Vegan Alternative"], data_cleaned["Gender"]
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Importance of Vegan Alternative by Gender
ax2 = sns.countplot(
    x="Importance of Vegan Alternative", data=data_cleaned, color="grey", ax=axes[1, 0]
)
ax2 = sns.countplot(
    x="Importance of Vegan Alternative",
    hue="Gender",
    data=data_cleaned,
    palette=palette,
    ax=axes[1, 0],
)
add_total_to_legend(ax2)
ax2.set_title(f"Importance of Vegan Alternative by Gender (p-value: {p_value:.2f})")
ax2.set_xlabel("Importance Level")
ax2.set_ylabel("Count")
ax2.tick_params(axis="x", rotation=0)

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Importance of Low Calories"], data_cleaned["Gender"]
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Importance of Low Calories by Gender
ax3 = sns.countplot(
    x="Importance of Low Calories", data=data_cleaned, color="grey", ax=axes[1, 1]
)
ax3 = sns.countplot(
    x="Importance of Low Calories",
    hue="Gender",
    data=data_cleaned,
    palette=palette,
    ax=axes[1, 1],
)
add_total_to_legend(ax3)
ax3.set_title(f"Importance of Low Caloriess by Gender (p-value: {p_value:.2f})")
ax3.set_xlabel("Importance Level")
ax3.set_ylabel("Count")
ax3.tick_params(axis="x", rotation=0)

# Adjust spacing between plots
plt.tight_layout()

# Show the plots
# plt.show()

tittle = "Product Characteristics"
plt.savefig(f"{save_path}{tittle} plot.png")

# ------------------------------ Distribution Channels and Price------------------------------


fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Likelihood of Buying Iced Latte"],
    data_cleaned["Residence Environment"],
)
_, p_value, _, _ = chi2_contingency(contingency_table)
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
ax0.set_title(
    f"Likelihood of Buying it in Supermarkets by Importance Level (p-value: {p_value:.2f})"
)
ax0.set_xlabel("Importance Level")
ax0.set_ylabel("Count")
ax0.tick_params(axis="x", rotation=0)

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Preferred Purchase Location"],
    data_cleaned["Residence Environment"],
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Preferred Purchase Location by Residence Environment
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
ax1.set_title(
    f"Preferred Purchase Location by Residence Environment (p-value: {p_value:.2f})"
)
ax1.set_xlabel("Place")
ax1.set_ylabel("Count")
ax1.tick_params(axis="x", rotation=0)

# Adjust spacing between plots
plt.tight_layout()

# Show the plots
# plt.show()

tittle = "Distribution Channels"
plt.savefig(f"{save_path}{tittle} plot.png")


fig, axes = plt.subplots(1, 3, figsize=(16, 6))

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Importance of Price"],
    data_cleaned["Current Situation"],
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Importance of Price by Current Situation
ax1 = sns.countplot(
    x="Importance of Price", data=data_cleaned, color="grey", ax=axes[0]
)
ax1 = sns.countplot(
    x="Importance of Price",
    hue="Current Situation",
    data=data_cleaned,
    ax=axes[0],
)
add_total_to_legend(ax1)
ax1.set_title(f"Importance of Price by Current Situation (p-value: {p_value:.2f})")
ax1.set_xlabel("Importance Level")
ax1.set_ylabel("Count")
ax1.tick_params(axis="x", rotation=0)

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Too Expensive Price Range"],
    data_cleaned["Current Situation"],
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Too Expensive Price Range by Current Situation
ax2 = sns.countplot(
    x="Too Expensive Price Range", data=data_cleaned, color="grey", ax=axes[1]
)
ax2 = sns.countplot(
    x="Too Expensive Price Range",
    hue="Current Situation",
    data=data_cleaned,
    ax=axes[1],
)
add_total_to_legend(ax2)
ax2.set_title(
    f"Too Expensive Price Range by Current Situation (p-value: {p_value:.2f})"
)
ax2.set_xlabel("Price Range")
ax2.set_ylabel("Count")
ax2.tick_params(axis="x", rotation=45)

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Too Cheap Price Range"],
    data_cleaned["Current Situation"],
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Too Cheap Price Range by Current Situation
ax3 = sns.countplot(
    x="Too Cheap Price Range", data=data_cleaned, color="grey", ax=axes[2]
)
ax3 = sns.countplot(
    x="Too Cheap Price Range",
    hue="Current Situation",
    data=data_cleaned,
    ax=axes[2],
)
add_total_to_legend(ax3)
ax3.set_title(f"Too Cheap Price Range by Current Situation (p-value: {p_value:.2f})")
ax3.set_xlabel("Price Range")
ax3.set_ylabel("Count")
ax3.tick_params(axis="x", rotation=45)

# Adjust spacing between plots
plt.tight_layout()

# Show the plots
# plt.show()

tittle = "Price"
plt.savefig(f"{save_path}{tittle} plot.png")

# ------------------------------ Idea Validation ------------------------------

fig, axes = plt.subplots(2, 4, figsize=(24, 12))

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Importance of Brand"],
    data_cleaned["Current Situation"],
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Importance of Brand by Current Situation
ax0 = sns.countplot(
    x="Importance of Brand", data=data_cleaned, color="grey", ax=axes[0, 0]
)
ax0 = sns.countplot(
    x="Importance of Brand",
    hue="Current Situation",
    data=data_cleaned,
    ax=axes[0, 0],
)
add_total_to_legend(ax0)
ax0.set_title(f"Importance of Brand by Current Situation (p-value: {p_value:.2f})")
ax0.set_xlabel("Importance Level")
ax0.set_ylabel("Count")
ax0.tick_params(axis="x", rotation=0)

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Importance of Brand"],
    data_cleaned["Residence Environment"],
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Importance of Brand by Residence Environment
ax1 = sns.countplot(
    x="Importance of Brand", data=data_cleaned, color="grey", ax=axes[1, 0]
)
ax1 = sns.countplot(
    x="Importance of Brand",
    hue="Residence Environment",
    data=data_cleaned,
    ax=axes[1, 0],
)
add_total_to_legend(ax1)
ax1.set_title(f"Importance of Brand by Residence Environment (p-value: {p_value:.2f})")
ax1.set_xlabel("Importance Level")
ax1.set_ylabel("Count")
ax1.tick_params(axis="x", rotation=0)


# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Specialness of Product Idea"],
    data_cleaned["Current Situation"],
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Specialness of Product Idea by Current Situation
ax0 = sns.countplot(
    x="Specialness of Product Idea", data=data_cleaned, color="grey", ax=axes[0, 1]
)
ax0 = sns.countplot(
    x="Specialness of Product Idea",
    hue="Current Situation",
    data=data_cleaned,
    ax=axes[0, 1],
)
add_total_to_legend(ax0)
ax0.set_title(
    f"Specialness of Product Idea by Current Situation (p-value: {p_value:.2f})"
)
ax0.set_xlabel("Specialness Level")
ax0.set_ylabel("Count")
ax0.tick_params(axis="x", rotation=0)


# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Specialness of Product Idea"],
    data_cleaned["Residence Environment"],
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Specialness of Product Idea by Age
ax1 = sns.countplot(
    x="Specialness of Product Idea", data=data_cleaned, color="grey", ax=axes[1, 1]
)
ax1 = sns.countplot(
    x="Specialness of Product Idea",
    hue="Residence Environment",
    data=data_cleaned,
    ax=axes[1, 1],
)
add_total_to_legend(ax1)
ax1.set_title(f"Specialness of Product Idea by Age Range (p-value: {p_value:.2f})")
ax1.set_xlabel("Specialness Level")
ax1.set_ylabel("Count")
ax1.tick_params(axis="x", rotation=0)


# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Importance of Ready-to-Drink Feature"],
    data_cleaned["Current Situation"],
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Importance of Ready-to-Drink Feature by Current Situation
ax2 = sns.countplot(
    x="Importance of Ready-to-Drink Feature",
    data=data_cleaned,
    color="grey",
    ax=axes[0, 2],
)
ax2 = sns.countplot(
    x="Importance of Ready-to-Drink Feature",
    hue="Current Situation",
    data=data_cleaned,
    ax=axes[0, 2],
)
add_total_to_legend(ax2)
ax2.set_title(
    f"Importance of Ready-to-Drink by Current Situation (p-value: {p_value:.2f})"
)
ax2.set_xlabel("Importance Level")
ax2.set_ylabel("Count")
ax2.tick_params(axis="x", rotation=0)


# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Importance of Ready-to-Drink Feature"],
    data_cleaned["Residence Environment"],
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Importance of Ready-to-Drink Feature by Age
ax3 = sns.countplot(
    x="Importance of Ready-to-Drink Feature",
    data=data_cleaned,
    color="grey",
    ax=axes[1, 2],
)
ax3 = sns.countplot(
    x="Importance of Ready-to-Drink Feature",
    hue="Residence Environment",
    data=data_cleaned,
    ax=axes[1, 2],
)
add_total_to_legend(ax3)
ax3.set_title(
    f"Importance of Ready-to-Drink by Residence Environment (p-value: {p_value:.2f})"
)
ax3.set_xlabel("Importance Level")
ax3.set_ylabel("Count")
ax3.tick_params(axis="x", rotation=0)

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Preferred Tea Flavor"],
    data_cleaned["Current Situation"],
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Preferred Tea Flavor by Current Situation
ax3 = sns.countplot(
    x="Preferred Tea Flavor", data=data_cleaned, color="grey", ax=axes[0, 3]
)
ax3 = sns.countplot(
    x="Preferred Tea Flavor", hue="Current Situation", data=data_cleaned, ax=axes[0, 3]
)
add_total_to_legend(ax3)
ax3.set_title(f"Preferred Flavor by Current Situation (p-value: {p_value:.2f})")
ax3.set_xlabel("Tea Flavor")
ax3.set_ylabel("Count")
ax3.tick_params(axis="x", rotation=45)

# Checking the p-value for the variable:
contingency_table = pd.crosstab(
    data_cleaned["Preferred Tea Flavor"],
    data_cleaned["Residence Environment"],
)
_, p_value, _, _ = chi2_contingency(contingency_table)
# Preferred Tea Flavor by Residence Environment
ax3 = sns.countplot(
    x="Preferred Tea Flavor", data=data_cleaned, color="grey", ax=axes[1, 3]
)
ax3 = sns.countplot(
    x="Preferred Tea Flavor",
    hue="Residence Environment",
    data=data_cleaned,
    ax=axes[1, 3],
)
add_total_to_legend(ax3)
ax3.set_title(f"Preferred Flavor by Residence Environment (p-value: {p_value:.2f})")
ax3.set_xlabel("Tea Flavor")
ax3.set_ylabel("Count")
ax3.tick_params(axis="x", rotation=45)

# Adjust spacing between plots
plt.tight_layout()

# Show the plots
# plt.show()

tittle = "Idea Validation"
plt.savefig(f"{save_path}{tittle} plot.png")
