from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.html import escape

class Pregunta(models.Model):

    id = models.BigAutoField(primary_key=True)   
    titulo = models.CharField(max_length=250)
    texto = models.CharField(max_length=5000)
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def clean(self):
        """Escapa el texto por si contiene caracteres HTML"""
        self.titulo = escape(self.titulo)
        self.texto = escape(self.texto)

    def __str__(self):
        """Para mostrar detalles en la interfaz admin"""
        return f"Pregunta({self.pk}, {self.titlo}, {self.texto}. {self.autor}, {self.fecha})"

class Respuesta(models.Model):

    id = models.BigAutoField(primary_key=True)
    texto = models.CharField(max_length=5000)
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)

    def clean(self):
        """Escapa el texto por si contiene caracteres HTML"""
        self.titulo = escape(self.titulo)
        self.texto = escape(self.texto)

    def __str__(self):
        """Para mostrar detalles en la interfaz admin"""
        return f"Respuesta({self.pk}, {self.pregunta}, {self.texto}. {self.autor}, {self.fecha})"