# comidas.py
# Recetas mexicanas comunes para la categoría "Comida"

Comidas = [
    {
        "nombre": "Pollo a la plancha con arroz y nopales",
        "ingredientes": {
            "proteina": ["Pechuga de pollo"],
            "carbohidrato": ["Arroz blanco cocido"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Nopales"]
        },
        "descripcion": "Pechuga de pollo a la plancha acompañada de arroz blanco y nopales asados."
    },
    {
        "nombre": "Carne molida con papa y calabacitas",
        "ingredientes": {
            "proteina": ["Carne magra"],
            "carbohidrato": ["Papas cocidas"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Calabacita", "Jitomate"]
        },
        "descripcion": "Carne molida magra guisada con papa y calabacitas, sazonada ligerito."
    },
    {
        "nombre": "Filete de res con arroz y espinacas",
        "ingredientes": {
            "proteina": ["Carne magra"],
            "carbohidrato": ["Arroz integral cocido"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Espinaca"]
        },
        "descripcion": "Filete de res sellado acompañado de arroz integral y espinacas salteadas."
    },
    {
        "nombre": "Pechuga de pollo en salsa verde con arroz",
        "ingredientes": {
            "proteina": ["Pechuga de pollo"],
            "carbohidrato": ["Arroz blanco cocido"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Calabacita", "Cebolla"]
        },
        "descripcion": "Pollo cocinado en salsa verde acompañado de arroz y calabacitas."
    },
    {
        "nombre": "Tacos de pechuga de pollo con verduras",
        "ingredientes": {
            "proteina": ["Pechuga de pollo"],
            "carbohidrato": ["Tortillas de maíz"],
            "grasa": ["Aguacate"],
            "vegetal": ["Lechuga", "Jitomate"]
        },
        "descripcion": "Tacos de pollo con lechuga, jitomate y aguacate."
    },
    {
        "nombre": "Salmón a la plancha con arroz y brócoli",
        "ingredientes": {
            "proteina": ["Salmón"],
            "carbohidrato": ["Arroz integral cocido"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Brócoli"]
        },
        "descripcion": "Salmón sellado acompañado de arroz integral y brócoli al vapor."
    },
    {
        "nombre": "Pollo a la mexicana con arroz",
        "ingredientes": {
            "proteina": ["Pechuga de pollo"],
            "carbohidrato": ["Arroz blanco cocido"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Jitomate", "Cebolla", "Chile verde"]
        },
        "descripcion": "Pechuga de pollo guisada con jitomate, cebolla y chile verde, acompañada de arroz."
    },
    {
        "nombre": "Atún guisado con verduras y arroz",
        "ingredientes": {
            "proteina": ["Atún en agua"],
            "carbohidrato": ["Arroz blanco cocido"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Zanahoria", "Calabacita"]
        },
        "descripcion": "Atún salteado con verduras picadas acompañado de arroz."
    },
    {
        "nombre": "Pavo a la plancha con puré de papa y espinaca",
        "ingredientes": {
            "proteina": ["Pavo"],
            "carbohidrato": ["Papas cocidas"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Espinaca"]
        },
        "descripcion": "Pavo a la plancha acompañado de puré de papa casero y espinaca salteada."
    },
    {
        "nombre": "Carne molida con arroz y nopales",
        "ingredientes": {
            "proteina": ["Carne magra"],
            "carbohidrato": ["Arroz integral cocido"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Nopales"]
        },
        "descripcion": "Carne molida guisada con nopales, servida con arroz integral."
    },
    {
        "nombre": "Pollo deshebrado con papas y salsa roja",
        "ingredientes": {
            "proteina": ["Pechuga de pollo"],
            "carbohidrato": ["Papas cocidas"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Jitomate", "Cebolla"]
        },
        "descripcion": "Pollo deshebrado guisado en salsa roja con papas cocidas."
    },
    {
        "nombre": "Carne asada con arroz y ensalada",
        "ingredientes": {
            "proteina": ["Carne magra"],
            "carbohidrato": ["Arroz blanco cocido"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Lechuga", "Jitomate"]
        },
        "descripcion": "Carne asada a la plancha acompañada de arroz blanco y ensalada fresca."
    },
    {
        "nombre": "Pechuga de pollo empapelada con verduras",
        "ingredientes": {
            "proteina": ["Pechuga de pollo"],
            "carbohidrato": ["Arroz blanco cocido"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Calabacita", "Zanahoria", "Cebolla"]
        },
        "descripcion": "Pechuga de pollo empapelada con verduras, servida con arroz."
    },
    {
        "nombre": "Pavo guisado con arroz y verduras",
        "ingredientes": {
            "proteina": ["Pavo"],
            "carbohidrato": ["Arroz integral cocido"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Zanahoria", "Chícharos"]
        },
        "descripcion": "Pavo guisado con verduras mixtas acompañado de arroz integral."
    },
    {
        "nombre": "Tinga de pollo con tostadas horneadas",
        "ingredientes": {
            "proteina": ["Pechuga de pollo"],
            "carbohidrato": ["Tostadas horneadas"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Cebolla", "Jitomate"]
        },
        "descripcion": "Tinga de pollo ligera servida sobre tostadas horneadas."
    },
    {
        "nombre": "Carne molida a la mexicana con arroz",
        "ingredientes": {
            "proteina": ["Carne magra"],
            "carbohidrato": ["Arroz blanco cocido"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Jitomate", "Cebolla", "Chile"]
        },
        "descripcion": "Carne molida guisada a la mexicana acompañada de arroz."
    },
    {
        "nombre": "Atún a la mexicana con arroz",
        "ingredientes": {
            "proteina": ["Atún en agua"],
            "carbohidrato": ["Arroz blanco cocido"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Jitomate", "Cebolla", "Chile"]
        },
        "descripcion": "Atún guisado a la mexicana servido con arroz blanco."
    },
    {
        "nombre": "Pollo en salsa de chipotle con arroz",
        "ingredientes": {
            "proteina": ["Pechuga de pollo"],
            "carbohidrato": ["Arroz integral cocido"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Cebolla"]
        },
        "descripcion": "Pollo guisado en salsa de chipotle acompañado de arroz integral."
    },
    {
        "nombre": "Filete de pescado al ajo con papas",
        "ingredientes": {
            "proteina": ["Filete de pescado"],
            "carbohidrato": ["Papas cocidas"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Espinaca"]
        },
        "descripcion": "Filete de pescado al ajo servido con papas cocidas y espinaca."
    },
    {
        "nombre": "Bowl de arroz con pollo y verduras",
        "ingredientes": {
            "proteina": ["Pechuga de pollo"],
            "carbohidrato": ["Arroz blanco cocido"],
            "grasa": ["Aceite de oliva"],
            "vegetal": ["Brócoli", "Zanahoria"]
        },
        "descripcion": "Bowl de arroz con pollo a la plancha y verduras al vapor."
    }

]
