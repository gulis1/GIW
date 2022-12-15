from django.contrib import admin

# Register your models here.
from .models import Pregunta, Respuesta

admin.site.register(Pregunta)
admin.site.register(Respuesta)
