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


# -*- coding: utf-8 -*-

#
# CABECERA AQUI
#


from flask import Flask, request, render_template
from mongoengine import connect, Document, StringField, EmailField
from mongoengine.errors import DoesNotExist, ValidationError
from passlib.hash import argon2
import pyotp
from flask_qrcode import QRcode
# Resto de importaciones


app = Flask(__name__)
connect('giw_auth')

QRcode(app)



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

    if request.form["password"] != request.form["password2"]:
        return "Las contaseñas no coinciden."

    user_exisente = User.objects(user_id=request.form["nickname"])
    if user_exisente:
        return "El usuario ya existe."

    hashed_pass = argon2.hash(request.form["password"])

    user = User(user_id=request.form["nickname"],
                full_name = request.form["full_name"],
                country = request.form["country"],
                email = request.form["email"],
                passwd = hashed_pass,
                totp_secret = "secreto"
            )
    
    user.save()
    return f"Bienvenido usuario {user.full_name}"


@app.route('/change_password', methods=['POST'])
def change_password():
    
    try:

        user= User.objects.get(user_id=request.form["nickname"])
        if not argon2.verify(request.form["old_password"], user.passwd): 
            raise AssertionError("Las contraseñas no coinciden.")
        
        user.passwd = argon2.hash(request.form["new_password"])
        user.save()
            
    except (DoesNotExist, AssertionError):
        return "Usuario o contraseña incorrectas."

    return f"La contraseña del usuario {user.user_id} ha sido modificada."
 
           
@app.route('/login', methods=['POST'])
def login():
    try:

        user= User.objects.get(user_id=request.form["nickname"])
        if not argon2.verify(request.form["password"], user.passwd):
            raise AssertionError("Las contraseñas no coinciden.")

            
    except (DoesNotExist, AssertionError):
        return "Usuario o contraseña incorrectas."

    return f"Bienvenido {user.full_name}."
    

##############
# APARTADO 2 #
##############

# 
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR
#


@app.route('/signup_totp', methods=['POST'])
def signup_totp():
    if request.form["password"] != request.form["password2"]:
        return "Las contaseñas no coinciden."

    user_exisente = User.objects(user_id=request.form["nickname"])
    if user_exisente:
        return "El usuario ya existe."

    hashed_pass = argon2.hash(request.form["password"])
    

    user = User(user_id=request.form["nickname"],
                full_name = request.form["full_name"],
                country = request.form["country"],
                email = request.form["email"],
                passwd = hashed_pass,
                totp_secret = pyotp.random_base32()
            )
    try:
        user.save()
    except ValidationError as e:
        return e.message, 400

    return render_template("totp_signup_success.html", name=user.full_name, secret=f"otpauth://totp/GIWApp?secret={user.totp_secret}")
        

@app.route('/login_totp', methods=['POST'])
def login_totp():
    
    try:

        user = User.objects.get(user_id=request.form["nickname"])
        if not argon2.verify(request.form["password"], user.passwd):
            raise AssertionError("Las contraseñas no coinciden.")
        
        totp = pyotp.TOTP(user.totp_secret)
        if not totp.verify(request.form["totp"]):
            raise AssertionError("El TOTP no coincide.")


            
    except (DoesNotExist, AssertionError):
        return "Usuario o contraseña incorrectas."

    return f"Bienvenido {user.full_name}."
  

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
