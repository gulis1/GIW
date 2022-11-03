"""
GIW 2022-23
Práctica NN
Grupo XX
Autores: XX, YY, ZZ,

(Nombres completos de los autores) declaramos que esta solución es fruto exclusivamente
de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
"""
from flask import Flask, request, session, render_template
app = Flask(__name__)


###
### <DEFINIR AQUI EL SERVICIO REST>
###


class FlaskConfig:
    """Configuración de Flask"""
    # Activa depurador y recarga automáticamente
    ENV = 'development'
    DEBUG = True
    TEST = True
    # Imprescindible para usar sesiones
    SECRET_KEY = "giw_clave_secreta"
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


if __name__ == '__main__':
    app.config.from_object(FlaskConfig())
    app.run()

