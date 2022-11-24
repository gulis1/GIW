# -*- coding: utf-8 -*-

"""
GIW 2022-23
Práctica 9
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


from flask import Flask, request, session, render_template
from mongoengine import connect, Document, StringField, EmailField
# Resto de importaciones


app = Flask(__name__)
connect('giw_auth')


# Clase para almacenar usuarios usando mongoengine
class User(Document):
    user_id = StringField(primary_key=True)
    full_name = StringField(min_length=2, max_length=50, required=True)
    country = StringField(min_length=2, max_length=50, required=True)
    email = EmailField(required=True)
    passwd = StringField(required=True)
    totp_secret = StringField(required=False)


##############
# APARTADO 1 #
##############

# 
# Explicación detallada del mecanismo escogido para el almacenamiento de
# contraseñas, explicando razonadamente por qué es seguro
#


@app.route('/signup', methods=['POST'])
def signup():
    ...


@app.route('/change_password', methods=['POST'])
def change_password():
    ...
 
           
@app.route('/login', methods=['POST'])
def login():
    ...
    

##############
# APARTADO 2 #
##############

# 
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR
#


@app.route('/signup_totp', methods=['POST'])
def signup_totp():
    ...
        

@app.route('/login_totp', methods=['POST'])
def login_totp():
    ...
  

class FlaskConfig:
    """Configuración de Flask"""
    # Activa depurador y recarga automáticamente
    ENV = 'development'
    DEBUG = True
    TEST = True
    # Imprescindible para usar sesiones
    SECRET_KEY = 'la_asignatura_de_giw'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


if __name__ == '__main__':
    app.config.from_object(FlaskConfig())
    app.run()
