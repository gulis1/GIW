import sys
from mongoengine import connect
connect('giw_mongoengine')

class Usuario(Document):
    dni = StringField(required=True, unique=True, min_length = 9, max_length = 9, regex = "[0-9]{8}[A-Z]")
    nombre = StringField(required=True, min_length = 2)  
    apellido1 = StringField(required=True, min_length = 2)  
    apellido2 = StringField(required=False, min_length = 2)
    f_nac = StringField(required=True, regex = "^[0-9]{4}-[0-1]{1}[0-9]{1}-[0-3]{1}[0-9]{1}$")
    tarjetas = ListField(required=False, EmbeddedDocumentField(Tarjeta))
    pedidos = ListField(required = False, ReferenceField(Pedido))

class Linea(EmbeddedDocument):
    num_items = IntField(required = True, min_value = 0)
    precio_item = FloatField(required = True, min_value=0)
    nombre_item: StringField(required=True, min_length = 2) 
    total = FloatField(required = True, min_value=0)
    ref = ReferenceField(required=True, Producto)
    