from typing import List, Dict
from tortoise import fields, models
import json


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
