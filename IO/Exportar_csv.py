import csv
from io import StringIO
import pandas as pd
import os

# Datos basados en la imagen proporcionada por el usuario
data = [
    ["Error Muestral (%)", "5.000", "10.000", "20.000", "40.000", "𝑥̄"],
    ["2%", 1667, 2000, 2222, 2353, 2500],
    ["3%", 909, 1000, 1053, 1081, 1112],
    ["4%", 556, 588, 606, 615, 625],
    ["5%", 370, 385, 392, 396, 400],
    ["6%", 263, 270, 274, 276, 278],
    ["7%", 198, 200, 202, 203, 204],
]

# Convertir los datos a un DataFrame de pandas
df = pd.DataFrame(data[1:], columns=data[0])

# Guardar el DataFrame como un archivo CSV en el escritorio
desktop_path = os.path.join(
    os.path.join(os.environ["HOME"]), "Desktop"
)  # Esto es para Windows
csv_file_path = os.path.join(desktop_path, "data.csv")
df.to_csv(csv_file_path, index=False)
