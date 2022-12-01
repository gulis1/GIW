# -*- coding: utf-8 -*-

#
# CABECERA AQUI
#

from flask import Flask, request, session
# Resto de importaciones


app = Flask(__name__)


# Credenciales. 
# https://developers.google.com/identity/openid-connect/openid-connect#appsetup
# Copiar los valores adecuados.
CLIENT_ID = XXXXXX
CLIENT_SECRET = YYYYYY

REDIRECT_URI = 'http://localhost:5000/token'

# Fichero de descubrimiento para obtener el 'authorization endpoint' y el 
# 'token endpoint'
# https://developers.google.com/identity/openid-connect/openid-connect#authenticatingtheuser
DISCOVERY_DOC = 'https://accounts.google.com/.well-known/openid-configuration'

# token_info endpoint para extraer información de los tokens en depuracion, sin
# descifrar en local
# https://developers.google.com/identity/openid-connect/openid-connect#validatinganidtoken
TOKENINFO_ENDPOINT = 'https://oauth2.googleapis.com/tokeninfo'


@app.route('/login_google', methods=['GET'])
def login_google():
    ...


@app.route('/token', methods=['GET'])
def token():
    ...

        
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
