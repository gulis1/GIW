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
from crypt import methods
import json
from flask import Flask, request, session, render_template
app = Flask(__name__)

DIAS_SEMANA = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

lista_asignaturas = []
next_id = 0

def horario_valido(horario: list) -> bool:
    
    try:
        for clase in horario:
            
            if len(clase) > 3: raise KeyError()
            if clase["dia"] not in DIAS_SEMANA: raise ValueError()
            elif clase["hora_inicio"] < 0 or clase["hora_inicio"] > 23: raise ValueError()
            elif clase["hora_final"] < 0 or clase["hora_final"] > 23: raise ValueError()

    except (KeyError, TypeError, ValueError) as e:
        return False
    
    return True

# Comprueba si una asignatura es correcta o no.
def comprobar_asignatura(asignatura: dict) -> str or None:
    
    if len(asignatura) > 3:
        return "Demasiados campos"

    if type(asignatura.get("nombre")) != str:
        return "Nombre no valido."
    
    if type(asignatura.get("numero_alumnos")) != int or asignatura["numero_alumnos"] < 0:
        return "Numero de alumnos no valido."

    if not horario_valido(asignatura.get("horario")):
        return "Horario no valido."

    
    
###
### <DEFINIR AQUI EL SERVICIO REST>
###
@app.route("/asignaturas", methods=["POST"])
def asignaturas_post():
    global next_id, lista_asignaturas

    nueva_as = request.get_json()
    error = comprobar_asignatura(nueva_as)

    if error is None:
        nueva_as["id"] = next_id
        next_id += 1
        lista_asignaturas.append(nueva_as)

        return (f"{json.dumps({'id': nueva_as['id']})}\n", 201)


    else:  return (f"{json.dumps({'error': error})}\n", 400)


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


