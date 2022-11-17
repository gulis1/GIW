from mongoengine import *

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
            print(correcto)
            raise ValidationError('Código de barras incorrecto.')

class Linea(EmbeddedDocument):

    nombre_item = StringField(required=True, min_length = 2) 
    num_items = IntField(required = True, min_value = 1)
    precio_item = FloatField(required = True, min_value=0)
    total = FloatField(required = True, min_value=0)
    ref = ReferenceField(Producto, required=True)

    def clean(self):
        self.validate(clean=False)
        
        if self.total != self.num_items * self.precio_item:
            raise ValidationError('Código de barras incorrecto.')


class Pedido(Document):
    total = IntField(required=True, min_value=0)
    fecha = ComplexDateTimeField(reuired=True)
    lineas = ListField(EmbeddedDocumentField(Linea), required=True)

class Usuario(Document):
    dni = StringField(required=True, unique=True, min_length = 9, max_length = 9, regex = "[0-9]{8}[A-Z]")
    nombre = StringField(required=True, min_length = 2)  
    apellido1 = StringField(required=True, min_length = 2)  
    apellido2 = StringField(required=False, min_length = 2)
    f_nac = StringField(required=True, regex = "^[0-9]{4}-[0-1]{1}[0-9]{1}-[0-3]{1}[0-9]{1}$")
    tarjetas = ListField(EmbeddedDocumentField(Tarjeta), required=False)
    pedidos = ListField(ReferenceField(Pedido), required = False)
