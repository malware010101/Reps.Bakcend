from typing import List, Dict
from tortoise import fields, models
from datetime import timezone
import json

# usuarios modelos


class User(models.Model):
    id = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, unique=True)
    password_hash = fields.CharField(max_length=100)
    rol = fields.CharField(max_length=20)

    def __str__(self):
        return self.nombre

    class Meta:
        table = "users"


class ProgramaEntrenamiento(models.Model):
    id = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=100)
    objetivo = fields.CharField(max_length=50)
    categoria = fields.CharField(max_length=50)
    nivel = fields.IntField()
    duracion_semanas = fields.IntField(default=4)
    dias_entrenamiento = fields.IntField(default=3)
    tipo = fields.CharField(max_length=20, default='base')

    dias_json = fields.TextField()

    creador = fields.ForeignKeyField(
        'models.User', related_name='programas_creados')

    is_general = fields.BooleanField(default=True)

    class Meta:
        table = "programas_entrenamiento"

    def get_dias(self) -> List[Dict]:
        if self.dias_json:
            return json.loads(self.dias_json)
        return []

    @classmethod
    async def create(cls, **kwargs):

        if 'dias' in kwargs:
            kwargs['dias_json'] = json.dumps(kwargs.pop('dias'))
        return await super().create(**kwargs)


# nutricion Modelos
class PlanNutricion(models.Model):
    id = fields.IntField(pk=True)
    usuario_id = fields.IntField(index=True)

    calorias_diarias = fields.IntField()

    macronutrientes = fields.JSONField()
    opciones_menu = fields.JSONField()
    datos_recibidos = fields.JSONField()

    activo = fields.BooleanField(default=True)
    creado_en = fields.DatetimeField(null=True)

    fecha_inicio = fields.DatetimeField(null=True)
    fecha_fin = fields.DatetimeField(null=True)
    estado = fields.CharField(max_length=20, default="activo")

    class Meta:
        table = "planes_nutricion"


class EntrenamientoActivo(models.Model):
    id = fields.IntField(pk=True)

    usuario = fields.ForeignKeyField(
        "models.User",
        related_name="entrenamientos_activos",
        on_delete=fields.CASCADE
    )

    programa = fields.ForeignKeyField(
        "models.ProgramaEntrenamiento",
        related_name="entrenamientos_asignados",
        on_delete=fields.CASCADE
    )
    tipo = fields.CharField(max_length=20)

    fecha_inicio = fields.DatetimeField(null=True)
    fecha_fin = fields.DatetimeField(null=True)

    fecha_asignacion = fields.DatetimeField(auto_now_add=True)
    activo = fields.BooleanField(default=True)

    class Meta:
        table = "entrenamientos_activos"


# Histroial de entrenamientos realizados por el usuario
class EntrenamientoHistorico(models.Model):
    id = fields.IntField(pk=True)

    usuario = fields.ForeignKeyField(
        "models.User",
        related_name="historial_entrenamientos",
        on_delete=fields.CASCADE
    )

    entrenamiento_activo = fields.ForeignKeyField(
        "models.EntrenamientoActivo",
        related_name="historial",
        on_delete=fields.CASCADE
    )

    programa_id = fields.IntField()
    programa_nombre = fields.CharField(max_length=100)

    dia_realizado = fields.CharField(max_length=30)

    completado_en = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "entrenamientos_historico"

# Historial de pesajes corporales


class PesajeHistorico(models.Model):
    id = fields.IntField(pk=True)

    usuario = fields.ForeignKeyField(
        "models.User",
        related_name="historial_pesajes",
        on_delete=fields.CASCADE
    )

    peso_kg = fields.FloatField()
    grasa_pct = fields.FloatField(null=True)
    masa_muscular_kg = fields.FloatField(null=True)
    imc = fields.FloatField(null=True)

    foto_frontal_url = fields.TextField(null=True)
    foto_izquierda_url = fields.TextField(null=True)
    foto_derecha_url = fields.TextField(null=True)
    foto_trasera_url = fields.TextField(null=True)

    registrado_en = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "pesajes_historico"


# ============================
# MODELOS CHAT
# ============================

class Chat(models.Model):
    id = fields.IntField(pk=True)

    # Usuario normal que inicia el chat
    usuario = fields.ForeignKeyField(
        "models.User",
        related_name="chats",
        on_delete=fields.CASCADE
    )

    creado_en = fields.DatetimeField(auto_now_add=True)
    activo = fields.BooleanField(default=True)

    class Meta:
        table = "chats"
        unique_together = ("usuario",)


class Mensaje(models.Model):
    id = fields.IntField(pk=True)

    chat = fields.ForeignKeyField(
        "models.Chat",
        related_name="mensajes",
        on_delete=fields.CASCADE
    )

    remitente = fields.ForeignKeyField(
        "models.User",
        related_name="mensajes_enviados",
        on_delete=fields.CASCADE
    )

    contenido = fields.TextField()

    leido = fields.BooleanField(default=False)

    enviado_en = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "mensajes"


class Anamnesis(models.Model):
    id = fields.IntField(pk=True)

    usuario = fields.OneToOneField(
        "models.User",
        related_name="anamnesis",
        on_delete=fields.CASCADE
    )

    datos = fields.JSONField()

    creada_en = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "anamnesis"
