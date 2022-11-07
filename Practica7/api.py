"""
GIW 2022-23
Práctica 7
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

def comprobar_asignatura(asignatura: dict) -> str or None:
    """Comprueba si una asignatura es correcta o no."""
    
    if len(asignatura) > 3:
        return "Demasiados campos"

    if type(asignatura.get("nombre")) != str:
        return "Nombre no valido."
    
    if type(asignatura.get("numero_alumnos")) != int or asignatura["numero_alumnos"] < 0:
        return "Numero de alumnos no valido."

    if not horario_valido(asignatura.get("horario")):
        return "Horario no valido."

def filtrar_asignaturas_url(alumnos_gte: int, page: int = None, per_page: int = None) -> tuple:
    """Retorna un diccionario con los url de las asignaturas que cumplen el requisito (si lo hay) de ser mayores que alumnos_gte. Si se especifica, se divide en páginas."""
    if(alumnos_gte == None):    #Valor por defecto
        alumnos_gte = 0

    pagina_asignaturas = None
    if(page != None and per_page != None):
        ini = (page - 1) * per_page
        fin = page*per_page
        # app.logger.info("Rango de elementos cogidos (ini-fin): "str(ini) + str(fin))
        pagina_asignaturas = lista_asignaturas[ini:fin]
    else:
        pagina_asignaturas = lista_asignaturas

    app.logger.info(pagina_asignaturas)
    urls = [f"/asignaturas/{x.get('id')}" for x in pagina_asignaturas if x.get("numero_alumnos") >= alumnos_gte]
    app.logger.info(alumnos_gte)

    code = None
    if(len(urls) < len(lista_asignaturas)):
        code = 206  #Partial content
    else:
        code = 200  #OK
    return ({"asignaturas": urls}, code)
    
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


    else:  return ("", 400)

@app.route("/asignaturas", methods=['DELETE'])
def eliminar_asignaturas():
    """Borra todas las asignaturas que pudieran existir. Devuelve el código 204 No Content"""
    #Borrar (resetear el diccionario de asignaturas)
    global lista_asignaturas
    lista_asignaturas = list()
    return ("", 204)


@app.route("/asignaturas", methods=['GET'])
def acceder_asignatura():
    """Devuelve un JSON con las URLs de la asignatura. Si no se especifica la asignatura se devuelven todas."""
    page = request.args.get('page')
    page = int(page) if page else page  #Convert to int if not None

    per_page = request.args.get('per_page')
    per_page = int(per_page) if per_page else per_page

    alumnos_gte = request.args.get('alumnos_gte')   #Alumnos greater or equal to this value
    alumnos_gte = int(alumnos_gte) if alumnos_gte else alumnos_gte

    if(page == None and per_page == None):
        return filtrar_asignaturas_url(alumnos_gte)
    elif(page != None and per_page != None):
        return filtrar_asignaturas_url(alumnos_gte, page, per_page)
    elif (page == None and per_page != None):
        return ("Debe introducirse el parámetro page si se introduce el parámetro per_page\n", 400)
    elif (page != None and per_page == None):
        return ("Debe introducirse el parámetro per_page si se introduce el parámetro page\n", 400)
        

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


