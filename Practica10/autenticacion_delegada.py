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

from flask import Flask, request, session, render_template
import requests
import json
import jwt
# Resto de importaciones


app = Flask(__name__)

# Credenciales. 
# https://developers.google.com/identity/openid-connect/openid-connect#appsetup
# Copiar los valores adecuados.
with open("credentials.json", mode="r") as file:
    creds = json.load(file)
    CLIENT_ID = creds["client_id"]
    CLIENT_SECRET = creds["client_secret"]



REDIRECT_URI = 'http://localhost:5000/token'

# Fichero de descubrimiento para obtener el 'authorization endpoint' y el 
# 'token endpoint'
# https://developers.google.com/identity/openid-connect/openid-connect#authenticatingtheuser
DISCOVERY_DOC = 'https://accounts.google.com/.well-known/openid-configuration'

# token_info endpoint para extraer información de los tokens en depuracion, sin
# descifrar en local
# https://developers.google.com/identity/openid-connect/openid-connect#validatinganidtoken
TOKENINFO_ENDPOINT = 'https://oauth2.googleapis.com/tokeninfo'

with requests.get(DISCOVERY_DOC) as r:
    AUTH_URL = f"{r.json()['authorization_endpoint']}?client_id={CLIENT_ID}&response_type=code&scope=openid%20email&redirect_uri={REDIRECT_URI}"
    TOKEN_URL = f"{r.json()['token_endpoint']}?client_secret={CLIENT_SECRET}&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&grant_type=authorization_code"

@app.route('/login_google', methods=['GET'])
def login_google():
    return render_template("login.html", auth_url=AUTH_URL)


@app.route('/token', methods=['GET'])
def token():
    code = request.args["code"]
    response = requests.post(f"{TOKEN_URL}&code={code}")

    id_token = response.json()["id_token"]
    # Esta url no esta en el discovery
    token_info = requests.get(f"{TOKENINFO_ENDPOINT}?id_token={id_token}").json()
    return f"Bienvenido {token_info['email']}"

        
class FlaskConfig:
    '''Configuración de Flask'''
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
