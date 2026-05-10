from typing import List, Dict
from tortoise import fields, models
from datetime import timezone
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
