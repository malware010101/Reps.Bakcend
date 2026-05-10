# app/services/recetas/colaciones.py


COLACIONES_PERDIDA_GRASA = [

    {
        "nombre": "Pepinos con limón y sal",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": [],
            "grasa": [],
            "vegetal": ["Pepino"]
        },
        "descripcion": "Pepino fresco en rodajas con limón y una pizca de sal."
    },

    {
        "nombre": "Gelatina light con fruta",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": ["Fresas"],
            "grasa": [],
            "vegetal": []
        },
        "descripcion": "Gelatina baja en calorías con fresas picadas."
    },

    {
        "nombre": "Queso panela con jitomate",
        "ingredientes": {
            "proteina": ["Queso panela"],
            "carbohidrato": [],
            "grasa": [],
            "vegetal": ["Jitomate"]
        },
        "descripcion": "Cubos de queso panela acompañados de jitomate fresco."
    },

    {
        "nombre": "Rollitos de jamón de pavo con queso panela",
        "ingredientes": {
            "proteina": ["Pavo", "Queso panela"],
            "carbohidrato": [],
            "grasa": [],
            "vegetal": ["Lechuga"]
        },
        "descripcion": "Rollitos de jamón de pavo con queso panela y lechuga."
    },

    {
        "nombre": "Claras de huevo con jitomate",
        "ingredientes": {
            "proteina": ["Claras de huevo"],
            "carbohidrato": [],
            "grasa": [],
            "vegetal": ["Jitomate"]
        },
        "descripcion": "Claras de huevo cocidas con jitomate."
    }

]

COLACIONES_MANTENIMIENTO = [
    {
        "nombre": "Yogurt griego con fresas y nueces",
        "ingredientes": {
            "proteina": ["Yogurt griego"],
            "carbohidrato": ["Fresas"],
            "grasa": ["Nueces mixtas"],
            "vegetal": []
        },
        "descripcion": "Yogurt griego natural con fresas y nueces."
    },

    {
        "nombre": "Manzana con crema de cacahuate",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": ["Manzana"],
            "grasa": ["Mantequilla de maní"],
            "vegetal": []
        },
        "descripcion": "Rebanadas de manzana con crema de cacahuate."
    },

    {
        "nombre": "Pan integral con aguacate",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": ["Pan integral"],
            "grasa": ["Aguacate"],
            "vegetal": []
        },
        "descripcion": "Pan integral tostado con aguacate machacado."
    },

    {
        "nombre": "Yogurt griego natural",
        "ingredientes": {
            "proteina": ["Yogurt griego"],
            "carbohidrato": [],
            "grasa": [],
            "vegetal": []
        },
        "descripcion": "Yogurt griego natural alto en proteína."
    },

    {
        "nombre": "Queso panela con manzana",
        "ingredientes": {
            "proteina": ["Queso panela"],
            "carbohidrato": ["Manzana"],
            "grasa": [],
            "vegetal": []
        },
        "descripcion": "Combinación de queso panela con manzana."
    }
]


COLACIONES_HIPERTROFIA = [
    {
        "nombre": "Smoothie de plátano con proteína",
        "ingredientes": {
            "proteina": ["Proteína en polvo"],
            "carbohidrato": ["Plátano"],
            "grasa": [],
            "vegetal": []
        },
        "descripcion": "Licuado de plátano con proteína."
    },

    {
        "nombre": "Avena con leche",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": ["Avena"],
            "grasa": [],
            "vegetal": []
        },
        "descripcion": "Avena preparada con agua o leche."
    },

    {
        "nombre": "Nueces mixtas con plátano",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": ["Plátano"],
            "grasa": ["Nueces mixtas"],
            "vegetal": []
        },
        "descripcion": "Nueces mixtas acompañadas de plátano."
    },

    {
        "nombre": "Pan integral con crema de cacahuate",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": ["Pan integral"],
            "grasa": ["Mantequilla de maní"],
            "vegetal": []
        },
        "descripcion": "Pan integral con crema de cacahuate."
    },

    {
        "nombre": "Avena con plátano",
        "ingredientes": {
            "proteina": [],
            "carbohidrato": ["Avena", "Plátano"],
            "grasa": [],
            "vegetal": []
        },
        "descripcion": "Avena combinada con rodajas de plátano"
    }
]

COLACIONES_POR_OBJETIVO = {
    "Perdida de Grasa": COLACIONES_PERDIDA_GRASA,
    "Mantenimiento": COLACIONES_MANTENIMIENTO,
    "Hipertrofia": COLACIONES_HIPERTROFIA,
}
