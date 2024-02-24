import json
import os
import pandas as pd
import matplotlib.pyplot as plt

save_path = os.path.join(os.path.expanduser("~"), "Downloads")  # Path to save the plots

# Load the JSON data, adjusting for UTF-8 Byte Order Mark (BOM) if necessary
file_path = "/Users/carlosedm10/projects/college/DCOM/evolucion_de_la_deuda_publica_de_la_eurozona.json"
with open(file_path, "r", encoding="utf-8-sig") as file:
    data = json.load(file)

# Extracting the relevant 'Datos' for plotting
datos_list = data["Respuesta"]["Datos"]["Metricas"][0]["Datos"]

# Creating a DataFrame from the extracted data
df = pd.DataFrame(datos_list)

# Converting 'Agno' and 'Periodo' into a single datetime column for better plotting
# Assuming 'Trimestre X' corresponds to quarters, we map these to appropriate month-day values
quarter_mapping = {
    "Trimestre 1": "-01-01",
    "Trimestre 2": "-04-01",
    "Trimestre 3": "-07-01",
    "Trimestre 4": "-10-01",
}

df["Date"] = df["Agno"].astype(str) + df["Periodo"].map(quarter_mapping)
df["Date"] = pd.to_datetime(df["Date"])

# Plotting the data
plt.figure(figsize=(14, 8))
plt.plot(df["Date"], df["Valor"], marker="o", linestyle="-", color="blue")

plt.title("Evolución de la deuda pública en la eurozona")
plt.xlabel("Tiempo")
plt.ylabel("Deuda en % del PIB")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
# export plot to download path
plt.savefig(f"{save_path}/evolucion_de_la_deuda_publica_de_la_eurozona.png")
