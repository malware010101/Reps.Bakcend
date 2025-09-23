# app/services/alimentos.py

alimentos_sugeridos = {
    "proteina": [
        {"nombre": "Pechuga de pollo", "query": "chicken breast", "porcion_sugerida": 150},
        {"nombre": "Carne molida", "query": "ground beef", "porcion_sugerida": 120},
        {"nombre": "Filete de pescado", "query": "fish fillet", "porcion_sugerida": 150},
        {"nombre": "Atún", "query": "tuna", "porcion_sugerida": 100},
        {"nombre": "Huevo", "query": "egg", "porcion_sugerida": 100} # Aprox. 2 huevos grandes
    ],
    "carbohidrato": [
        {"nombre": "Arroz integral", "query": "brown rice", "porcion_sugerida": 80},
        {"nombre": "Avena", "query": "oats", "porcion_sugerida": 60},
        {"nombre": "Camote", "query": "sweet potato", "porcion_sugerida": 150},
        {"nombre": "Pasta", "query": "pasta", "porcion_sugerida": 80},
        {"nombre": "Pan integral", "query": "whole wheat bread", "porcion_sugerida": 50},
        {"nombre": "Frijoles", "query": "beans", "porcion_sugerida": 100}
    ],
    "grasa": [
        {"nombre": "Aguacate", "query": "avocado", "porcion_sugerida": 50},
        {"nombre": "Almendras", "query": "almonds", "porcion_sugerida": 30},
        {"nombre": "Aceite de oliva", "query": "olive oil", "porcion_sugerida": 15},
        {"nombre": "Nueces", "query": "walnuts", "porcion_sugerida": 30}
    ],
    "vegetales": [
        {"nombre": "Espinacas", "query": "spinach", "porcion_sugerida": 100},
        {"nombre": "Brócoli", "query": "broccoli", "porcion_sugerida": 100},
        {"nombre": "Lechuga", "query": "lettuce", "porcion_sugerida": 100},
        {"nombre": "Tomate", "query": "tomato", "porcion_sugerida": 100},
        {"nombre": "Pepino", "query": "cucumber", "porcion_sugerida": 100},
        { "nombre": "Esparragos", "query": "arugula", "porcion_sugerida": 100 }
    ],
    "snack": [
        {"nombre": "Manzana", "query": "apple", "porcion_sugerida": 100},
        {"nombre": "Yogur griego", "query": "greek yogurt", "porcion_sugerida": 100},
        {"nombre": "Plátano", "query": "banana", "porcion_sugerida": 120},
        {"nombre": "Almendras", "query": "almonds", "porcion_sugerida": 30},
        {"nombre": "Mantequilla de cacahuete", "query": "peanut butter", "porcion_sugerida": 20},
    ]
}
