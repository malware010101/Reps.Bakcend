from tortoise import fields
from tortoise.models import Model


class PlanNutricion(Model):
    id = fields.IntField(pk=True)
    usuario_id = fields.IntField(index=True)

    calorias_diarias = fields.IntField()

    macronutrientes = fields.JSONField()
    opciones_menu = fields.JSONField()
    datos_recibidos = fields.JSONField()

    activo = fields.BooleanField(default=True)
    creado_en = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "planes_nutricion"
