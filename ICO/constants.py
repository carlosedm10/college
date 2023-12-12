COLUMN_NAMES = {
    "Marca temporal": "Timestamp",
    "1. ¿Cuál de estos sabores de té latte helado le gustaría probar?": "Preferred Tea Flavor",
    "2. ¿Con qué frecuencia consume bebidas frías como tés, cafés, smoothies, batidos, etc.?\n": "Frequency of Cold Beverages",
    "3. ¿Comprarías un té frío con leche como Iced Latte Tea si estuviese en tu supermercado?\n": "Likelihood of Buying Iced Latte",
    "4. ¿Considera importante el aspecto de los ingredientes naturales al elegir Iced Latte? ": "Importance of Natural Ingredients",
    "5. ¿Considera importante el aspecto de bajo contenido calórico al elegir Iced Latte? ": "Importance of Low Calories",
    "6. ¿Considera importante la marca a la hora de elegir un Iced Latte? ": "Importance of Brand",
    "7. ¿Considera importante el precio al elegir Iced Latte? ": "Importance of Price",
    "8. ¿Considera importante el sabor al elegir Iced Latte? ": "Importance of Flavor",
    "9. ¿Cómo de especial es esta idea de producto para ti?": "Specialness of Product Idea",
    "10. ¿Cómo valora la importancia de que una bebida tenga su alternativa vegana?": "Importance of Vegan Alternative",
    '11. ¿Qué precios te parecen demasiado caros para un "Iced Latte Tea"?': "Too Expensive Price Range",
    '12. ¿Qué precios te parecen demasiado baratos para que "Iced Latte Tea" sea de buena calidad?': "Too Cheap Price Range",
    "13. ¿Dónde comprarías un Iced Latte Tea para consumir en la calle?": "Preferred Purchase Location",
    '14. ¿Cuál de las siguientes opciones reflejaría mejor su consumo de "Iced Latte Tea"?': "Iced Latte Tea Consumption Option",
    "15. ¿La opción vegana le resultaría atractiva para Iced Latte? ": "Control Question",
    "16. ¿Cómo de importante le parece la  característica “listo para consumir” en un Iced Latte Tea?": "Importance of Ready-to-Drink Feature",
    "17. ¿Cómo de importante es para ti encontrar alternativas al cafe?": "Importance of Finding Coffee Alternatives",
    "18. ¿La opción de que sea saludable le resultaría atractiva para Iced Latte? ": "Attractiveness of Healthy Option",
    "19. ¿Cuál es su rango de edad?": "Age Range",
    "20. ¿Cuál es su género?": "Gender",
    "21. ¿Cuál es su situación actual?": "Current Situation",
    "22. ¿Cuál es el entorno de su lugar de residencia actual?": "Residence Environment",
}

# Define the mapping
IMPORTANCE_MAPPING = {
    "Muy importante": 5,
    "Importante": 4,
    "Algo importante": 3,
    "Poco importante": 2,
    "Nada importante": 1,
}

FRECUENCY_MAPPING = {
    "Diariamente": 5,
    "3 o 4 veces a la semana": 4,
    "1 o 2 veces a la semana": 3,
    "Raramente": 2,
    "Nunca": 1,
}

FRECUENCY_MAPPING_2 = {
    "Consumiría diariamente": 4,
    "Consumiría varias veces a la semana": 3,
    "Consumiría solo ocasionalmente": 2,
    'No estoy interesado/a en consumir "iced latte tea"': 1,
}

LIKELIHOOD_MAPPING = {
    "Absolutamente sí": 5,
    "Probablemente sí": 4,
    "Indiferente": 3,
    "Probablemente no": 2,
    "Absolutamente no": 1,
}
