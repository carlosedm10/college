# Define the detailed tasks with adjusted timelines for parones and more programming
from matplotlib import pyplot as plt
from matplotlib.dates import date2num
import pandas as pd
import matplotlib.dates as mdates


tasks_adjusted = [
    {
        "Task": "Lectura y redacción de la introducción",
        "Start": "2024-08-01",
        "End": "2024-08-15",
        "Phase": "Introducción",
    },
    {
        "Task": "Investigación sobre conceptos básicos",
        "Start": "2024-08-16",
        "End": "2024-08-31",
        "Phase": "Marco Teórico",
    },
    {
        "Task": "Redacción sobre conceptos básicos",
        "Start": "2024-09-01",
        "End": "2024-09-15",
        "Phase": "Marco Teórico",
    },
    {
        "Task": "Recopilación de datos y definiciones",
        "Start": "2024-08-01",
        "End": "2024-09-15",
        "Phase": "Marco Teórico",
    },
    {
        "Task": "Análisis de problemas del enfoque actual",
        "Start": "2024-09-16",
        "End": "2024-09-30",
        "Phase": "Marco Teórico",
    },
    {
        "Task": "Parón por exámenes",
        "Start": "2024-10-01",
        "End": "2024-10-15",
        "Phase": "Parón",
    },
    {
        "Task": "Estudio de variables dummy",
        "Start": "2024-10-16",
        "End": "2024-10-31",
        "Phase": "Estudio de Distribuciones",
    },
    {
        "Task": "Variables escalón y calendario",
        "Start": "2024-11-01",
        "End": "2024-11-15",
        "Phase": "Estudio de Distribuciones",
    },
    {
        "Task": "Investigación sobre modelos predictivos",
        "Start": "2024-11-16",
        "End": "2024-11-30",
        "Phase": "Estudio de Distribuciones",
    },
    {
        "Task": "Parón por exámenes",
        "Start": "2024-12-01",
        "End": "2024-12-15",
        "Phase": "Parón",
    },
    {
        "Task": "Desarrollo de nuevas métricas",
        "Start": "2024-12-16",
        "End": "2024-12-31",
        "Phase": "Propuestas de Mejora",
    },
    {
        "Task": "Lectura sobre técnicas avanzadas y ML",
        "Start": "2025-02-01",
        "End": "2025-02-15",
        "Phase": "Propuestas de Mejora",
    },
    {
        "Task": "Implementación de ML",
        "Start": "2025-02-16",
        "End": "2025-02-28",
        "Phase": "Propuestas de Mejora",
    },
    {
        "Task": "Parón por exámenes",
        "Start": "2025-01-01",
        "End": "2025-01-31",
        "Phase": "Parón",
    },
    {
        "Task": "Procesamiento de datos: limpieza y preparación",
        "Start": "2025-03-01",
        "End": "2025-03-31",
        "Phase": "Metodología",
    },
    {
        "Task": "Desarrollo de modelos estadísticos",
        "Start": "2025-04-01",
        "End": "2025-04-30",
        "Phase": "Metodología",
    },
    {
        "Task": "Implementación de redes neuronales y ML",
        "Start": "2025-05-01",
        "End": "2025-05-31",
        "Phase": "Metodología",
    },
    {
        "Task": "Parón por exámenes",
        "Start": "2025-05-16",
        "End": "2025-05-31",
        "Phase": "Parón",
    },
    {
        "Task": "Ejecución de back tests",
        "Start": "2025-06-01",
        "End": "2025-06-30",
        "Phase": "Validación y Pruebas",
    },
    {
        "Task": "Realización de simulaciones",
        "Start": "2025-07-01",
        "End": "2025-07-31",
        "Phase": "Validación y Pruebas",
    },
    {
        "Task": "Análisis de resultados",
        "Start": "2025-08-01",
        "End": "2025-08-10",
        "Phase": "Resultados",
    },
    {
        "Task": "Comparación con metodologías actuales",
        "Start": "2025-08-11",
        "End": "2025-08-20",
        "Phase": "Resultados",
    },
    {
        "Task": "Redacción de la discusión",
        "Start": "2025-08-21",
        "End": "2025-08-31",
        "Phase": "Resultados",
    },
    {
        "Task": "Redacción de conclusiones",
        "Start": "2025-09-01",
        "End": "2025-09-10",
        "Phase": "Conclusiones",
    },
    {
        "Task": "Revisión y edición final",
        "Start": "2025-09-11",
        "End": "2025-09-20",
        "Phase": "Revisión y Preparación",
    },
    {
        "Task": "Preparación de la presentación",
        "Start": "2025-09-21",
        "End": "2025-09-30",
        "Phase": "Revisión y Preparación",
    },
    {
        "Task": "Práctica de la presentación",
        "Start": "2025-10-01",
        "End": "2025-10-10",
        "Phase": "Revisión y Preparación",
    },
]

# Convert to DataFrame
df_adjusted = pd.DataFrame(tasks_adjusted)

# Convert date strings to datetime
df_adjusted["Start"] = pd.to_datetime(df_adjusted["Start"])
df_adjusted["End"] = pd.to_datetime(df_adjusted["End"])

# Calculate margin for each task
df_adjusted["Margin Start"] = df_adjusted["Start"] - pd.Timedelta(days=3)
df_adjusted["Margin End"] = df_adjusted["End"] + pd.Timedelta(days=3)

# Create a color map based on phases
phase_colors_adjusted = {
    "Introducción": "#1f77b4",
    "Marco Teórico": "#ff7f0e",
    "Estudio de Distribuciones": "#2ca02c",
    "Propuestas de Mejora": "#d62728",
    "Metodología": "#9467bd",
    "Validación y Pruebas": "#8c564b",
    "Resultados": "#e377c2",
    "Conclusiones": "#7f7f7f",
    "Revisión y Preparación": "#bcbd22",
    "Parón": "#17becf",
}

df_adjusted["Color"] = df_adjusted["Phase"].map(phase_colors_adjusted)

# Plotting
fig, ax = plt.subplots(figsize=(26, 12))

# Plot tasks with margins
for i, task in df_adjusted.iterrows():
    ax.barh(
        task["Task"],
        date2num(task["End"]) - date2num(task["Start"]),
        left=date2num(task["Start"]),
        color=task["Color"],
        edgecolor="black",
        alpha=0.6,
    )
    ax.barh(
        task["Task"],
        date2num(task["Margin End"]) - date2num(task["Margin Start"]),
        left=date2num(task["Margin Start"]),
        color=task["Color"],
        edgecolor="black",
        alpha=0.3,
    )

# Format the plot
ax.set_xlabel("Time")
ax.set_ylabel("Tasks")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
ax.xaxis.set_major_locator(mdates.MonthLocator())
plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
ax.set_title("Diagrama de Gantt Ajustado para el TFG")

plt.tight_layout()
plt.savefig("/Users/carlosedm10/downloads/diagrama_gantt_tfg_visual_adjusted.png")
