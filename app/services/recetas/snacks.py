# app/services/recetas/snacks.py


SNACKS_PERDIDA_GRASA = [

    {
        "nombre": "Pepinos con limón y sal",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": [],
            "grasa": [],
            "vegetal": ["Pepino"]
        },
        "descripcion": "Pepinos frescos en rodajas con limón y sal."
    },
    {
        "nombre": "Rebanadas de queso panela",
        "ingredientes": {
            "proteina": ["Queso panela"],
            "carbohidrato": [],
            "grasa": [],
            "vegetal": []
        },
        "descripcion": "Queso panela fresco en cubos."
    },

    {
        "nombre": "Yogurt griego natural",
        "ingredientes": {
            "proteina": ["Yogurt griego"],
            "carbohidrato": [],
            "grasa": [],
            "vegetal": []
        },
        "descripcion": "Yogurt griego natural sin azúcar."
    },

    {
        "nombre": "Batido de proteína con agua",
        "ingredientes": {
            "proteina": ["Proteína en polvo"],
            "carbohidrato": [],
            "grasa": [],
            "vegetal": []
        },
        "descripcion": "Batido de proteína preparado con agua."
    },

    {
        "nombre": "Gelatina light",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": [],
            "grasa": [],
            "vegetal": []
        },
        "descripcion": "Gelatina sin azúcar."
    }
]


SNACKS_MANTENIMIENTO = [
    {
        "nombre": "Manzana con mantequilla de maní",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": ["Manzana"],
            "grasa": ["Mantequilla de maní"],
            "vegetal": []
        },
        "descripcion": "Rodajas de manzana con mantequilla de maní."
    },

    {
        "nombre": "Pan tostado con aguacate",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": ["Pan integral"],
            "grasa": ["Aguacate"],
            "vegetal": []
        },
        "descripcion": "Pan integral tostado con aguacate machacado."
    },

    {
        "nombre": "Yogurt con fresas y nueces",
        "ingredientes": {
            "proteina": ["Yogurt griego"],
            "carbohidrato": ["Fresas"],
            "grasa": ["Nueces mixtas"],
            "vegetal": []
        },
        "descripcion": "Yogurt griego con fresas y nueces."
    },

    {
        "nombre": "Galletas de arroz con crema de maní",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": ["Galletas de arroz"],
            "grasa": ["Mantequilla de maní"],
            "vegetal": []
        },
        "descripcion": "Galletas de arroz con crema de maní."
    },

    {
        "nombre": "Taza de frutas mixtas",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": ["Manzana", "Plátano", "Mango"],
            "grasa": [],
            "vegetal": []
        },
        "descripcion": "Mix de frutas frescas."
    }
]


SNACKS_HIPERTROFIA = [
    {
        "nombre": "Batido de proteína con plátano",
        "ingredientes": {
            "proteina": ["Proteína en polvo"],
            "carbohidrato": ["Plátano"],
            "grasa": [],
            "vegetal": []
        },
        "descripcion": "Batido de proteína con plátano."
    },

    {
        "nombre": "Camote horneado",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": ["Camote"],
            "grasa": [],
            "vegetal": []
        },
        "descripcion": "Camote horneado en cubos."
    },

    {
        "nombre": "Palomitas caseras con aceite de oliva",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": ["Maíz palomero"],
            "grasa": ["Aceite de oliva"],
            "vegetal": []
        },
        "descripcion": "Palomitas naturales hechas en casa."
    },

    {
        "nombre": "Pan integral con mantequilla de maní",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": ["Pan integral"],
            "grasa": ["Mantequilla de maní"],
            "vegetal": []
        },
        "descripcion": "Pan integral con mantequilla de maní."
    },

    {
        "nombre": "Yogurt griego con avena",
        "ingredientes": {
            "proteina": ["Yogurt griego"],
            "carbohidrato": ["Avena"],
            "grasa": [],
            "vegetal": []
        },
        "descripcion": "Yogurt griego con avena."
    }
]

SNACKS_POR_OBJETIVO = {
    "Perdida de Grasa": SNACKS_PERDIDA_GRASA,
    "Mantenimiento": SNACKS_MANTENIMIENTO,
    "Hipertrofia": SNACKS_HIPERTROFIA,
}
