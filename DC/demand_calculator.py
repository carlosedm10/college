import pandas as pd
import numpy as np

# Load the Excel files
transition_matrix_path = "/Users/carlosedm10/projects/college/DC/transition_matrix.xlsx"
sales_data_path = "/Users/carlosedm10/projects/college/DC/sales.xlsx"


transition_matrix_pd = pd.read_excel(transition_matrix_path, sheet_name="Transition")
sales_pd = pd.read_excel(sales_data_path, sheet_name="Sales")

transition_matrix = transition_matrix_pd.iloc[0:32, 1:33].values
sales_vector = sales_pd.iloc[0:32, 1].values

products = sales_pd.iloc[0:32, 0].values

# Convert column vector to row vector
sales_vector = sales_vector.reshape(-1, 1)

# Perform the multiplication
result = np.dot(transition_matrix, sales_vector)

# Convert the result back to a DataFrame for easy viewing/saving
result_df = pd.DataFrame(result, columns=["Result"])

assert (
    result_df.size
    == products.size
    == sales_vector.size
    == transition_matrix.shape[0]
    == transition_matrix.shape[1]
)

result_df["Product"] = products
result_df = result_df.reindex(columns=["Product", "Result"])
# Print the result
print(f"Expected demand: \n{round(result_df)}")

# Save the result to a new Excel file
result_df.to_excel("/Users/carlosedm10/projects/college/DC/result.xlsx", index=False)
