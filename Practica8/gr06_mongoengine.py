"""
GIW 2022-23
Práctica 8
Grupo 6
Autores: (Roberto Tejedor Moreno, Julián Cámara Miró, Pablo Lozano Martín, Jun Qiu y
Jaime Pastrana García)

El grupo 6 (Roberto Tejedor Moreno, Julián Cámara Miró, Pablo Lozano Martín, Jun Qiu y
Jaime Pastrana García) declaramos que esta solución es fruto exclusivamente
de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
"""

from mongoengine import *

def dni_valid(num: int, l: str) -> bool:
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    return letras[num%23] == l

class Tarjeta(EmbeddedDocument):
    nombre = StringField(required=True, min_length=2)
    numero = StringField(required=True, regex="^[0-9]{16}$", primary_key=True)
    mes = StringField(required=True, regex="^((0[1-9])|(1[0-2]))$")
    año = StringField(required=True, regex="^[0-9]{2}$")
    ccv = StringField(required=True, regex="^[0-9]{3}$")


class Producto(Document):
    codigo_barras = StringField(required=True, regex="^[0-9]{13}$", primary_key=True)
    nombre = StringField(required=True)
    # nombre = StringField(required=True, regex="/^[a-z]|\s{2,}$/gi")

    categoria_principal = IntField(required=True, min_value=0)
    categorias_secundarias = ListField(IntField(min_value=0))

    def clean(self):
        self.validate(clean=False)
        
        suma_impar = suma_par = 0
        for i, dig in enumerate(reversed(self.codigo_barras[:-1])):
            if i%2 == 0:
                suma_impar += int(dig)
            else:
                suma_par += int(dig)

        suma = suma_impar * 3 + suma_par
        correcto = (10 - suma % 10) % 10

        if self.codigo_barras[-1] != str(correcto):
            raise ValidationError('Código de barras incorrecto.')

        if len(self.categorias_secundarias) > 0 and self.categoria_principal != self.categorias_secundarias[0]:
            raise ValidationError('Categorías secundarioas incorrectas.')



class Linea(EmbeddedDocument):

    nombre_item = StringField(required=True, min_length = 2) 
    num_items = IntField(required = True, min_value = 1)
    precio_item = FloatField(required = True, min_value=0)
    total = FloatField(required = True, min_value=0)
    ref = ReferenceField(Producto, required=True)

    def clean(self):
        self.validate(clean=False)
        
        if self.nombre_item != self.ref.nombre:
            raise ValidationError('El nombre del produco no coincide.')

        if self.total != self.num_items * self.precio_item:
            raise ValidationError('El precio total no es correcto.')


class Pedido(Document):
    total = FloatField(required=True, min_value=0)
    fecha = ComplexDateTimeField(required=True)
    lineas = ListField(EmbeddedDocumentField(Linea), required=True)

    def clean(self):
        self.validate(clean=False)
        
        if len(self.lineas) != len(set([linea.nombre_item for linea in self.lineas])):
            raise ValidationError('Hay dos líneas para el mismo producto.')

        if self.total != sum([linea.total for linea in self.lineas]):
            raise ValidationError('El precio total del pedido no es correcto.')



class Usuario(Document):
    dni = StringField(required=True, unique=True, min_length = 9, max_length = 9, regex = "[0-9]{8}[A-Z]")
    nombre = StringField(required=True, min_length = 2)  
    apellido1 = StringField(required=True, min_length = 2)  
    apellido2 = StringField(required=False, min_length = 2)
    f_nac = StringField(required=True, regex = "^[0-9]{4}-[0-1]{1}[0-9]{1}-[0-3]{1}[0-9]{1}$")
    tarjetas = ListField(EmbeddedDocumentField(Tarjeta), required=False)
    pedidos = ListField(ReferenceField(Pedido, reverse_delete_rule=PULL), required = False)
    
    def clean(self):
        self.validate(clean=False)
        num = int(self.dni[0:8])
        letra = self.dni[8]
        if(not dni_valid(num, letra)):
            raise ValidationError("DNI incorrecto: " + str(num) + ' ' + letra)

