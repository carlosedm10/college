import pandas as pd
import numpy as np
from PIL import Image
import pytesseract
import re

# Load the images
demand = "/demand.png"
sales = "/sales.png"

# Open images
demand = Image.open(demand)
sales = Image.open(sales)

# Perform OCR on the images
text_1 = pytesseract.image_to_string(demand)
text_2 = pytesseract.image_to_string(sales)


# Function to parse transition matrix text
def parse_transition_matrix(text):
    matrix = {}
    lines = text.strip().split("\n")
    for line in lines:
        key, values = line.split(":")
        key = key.strip()
        values = re.findall(r"[-+]?\d*\.\d+|\d+", values)
        values = [float(v) for v in values]
        matrix[key] = values
    return matrix


# Function to parse sales data text
def parse_sales_data(text):
    sales = {}
    lines = text.strip().split("\n")
    for line in lines:
        if ":" in line:
            key, value = line.split(":")
            key = key.strip()
            value = re.findall(r"[-+]?\d*\.\d+|\d+", value)[0]
            sales[key] = int(value)
    return sales


sales = parse_sales_data(text_2)

matrix = parse_transition_matrix(text_1)
