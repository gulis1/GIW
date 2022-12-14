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

#Funciones auxiliares
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
    """Comprueba si una asignatura es correcta o no. Devuelve un str con el mensaje del error si no es correcta."""
    
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

    asignaturas_filtradas = [x for x in lista_asignaturas if x.get("numero_alumnos") >= alumnos_gte]    #Se filtran

    pagina_asignaturas = None   #Se coge la página correspondiente
    if(page != None and per_page != None):
        ini = (page - 1) * per_page
        fin = page*per_page
        # app.logger.info("Rango de elementos cogidos (ini-fin): "str(ini) + str(fin))
        pagina_asignaturas = asignaturas_filtradas[ini:fin]
    else:
        pagina_asignaturas = asignaturas_filtradas

    #se generan las urls
    # app.logger.info(pagina_asignaturas)
    urls = [f"/asignaturas/{x.get('id')}" for x in pagina_asignaturas]
    # app.logger.info(f"Más de {alumnos_gte} alumnos")

    code = None
    if(len(urls) < len(lista_asignaturas)):
        code = 206  #Partial content
    else:
        code = 200  #OK
    return ({"asignaturas": urls}, code)
    
###
### <DEFINIR AQUI EL SERVICIO REST>
###
#2.1--
@app.route("/asignaturas", methods=['DELETE'])
def eliminar_asignaturas():
    """Borra todas las asignaturas que pudieran existir. Devuelve el código 204 No Content"""
    #Borrar (resetear el diccionario de asignaturas)
    global lista_asignaturas
    lista_asignaturas = list()
    return ("", 204)

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

@app.route("/asignaturas", methods=['GET'])
def acceder_asignaturas():
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

#2.2--
@app.route("/asignaturas/<int:id>", methods=['DELETE'])
def eliminar_asignatura(id: int):
    encontrada = False
    for asignatura in lista_asignaturas:
        if asignatura.get("id", -1) == id:
            lista_asignaturas.remove(asignatura)
            return ("", 204)

    return ("", 404)

@app.route("/asignaturas/<int:id>", methods=['GET'])
def acceder_asignatura(id: int):
    """Devuelve la asignatura de dicho id"""
    for asignatura in lista_asignaturas:
        if asignatura.get("id", -1) == id:
            return (asignatura, 200)

    return ("", 404)

@app.route("/asignaturas/<int:id>", methods=['PUT'])
def reemplazar_asignatura(id: int):
    """Modifica la asignatura de dicho id a los parámetros especificados"""

    asignatura_i = [i for i, a in enumerate(lista_asignaturas) if a.get("id", -1) == id]
    if len(asignatura_i) == 0:
        return ("", 404)    #No se encontró la asignatura
    elif len(asignatura_i) > 1:
        return ("Colisión de ids", 500)    #Si se llega a este caso es que algo ha fallado en el server (id repetido)
    else:
        asignatura_i = asignatura_i[0]

    nueva_as = request.get_json()
    error = comprobar_asignatura(nueva_as)

    if error is not None:
        return ("", 400)

    nueva_as["id"] = id
    lista_asignaturas[asignatura_i] = nueva_as
    return ("", 200)

@app.route("/asignaturas/<int:id>", methods=['PATCH'])
def cambiar_asignatura(id: int):

    asignatura_i = [i for i, a in enumerate(lista_asignaturas) if a.get("id", -1) == id]
    if len(asignatura_i) == 0:
        return ("", 404)    #No se encontró la asignatura
    elif len(asignatura_i) > 1:
        return ("Colisión de ids", 500)    #Si se llega a este caso es que algo ha fallado en el server (id repetido)
    else:
        asignatura_i = asignatura_i[0]

    campo = request.get_json()

    if(len(campo) != 1):    #Comrobar que es un único campo el que se quiere añadir
        return ("Len", 400)

    #Formar la nueva asignatura
    nueva_as = lista_asignaturas[asignatura_i]
    nueva_as.update(campo)

    nueva_as.pop("id")
    mensaje_e = comprobar_asignatura(nueva_as)
    nueva_as["id"] = id
    if (mensaje_e is not None):    #Comprobar que el campo introducido no hace que quede fuera de los límites
        # app.logger.info(nueva_as)
        # app.logger.error("Asignatura no válida: " + mensaje_e)
        return ("", 400)
    
    lista_asignaturas[asignatura_i] = nueva_as  #Aplicar el cambio
    return ("", 200)

#2.3--
@app.route("/asignaturas/<int:id>/horario", methods=['GET'])
def get_horario(id: int):
    """Devuelve el horario de la asignatura de dicho id."""
    for asignatura in lista_asignaturas:
        if asignatura.get("id", -1) == id:
            return ({"horario": asignatura.get("horario", [])}, 200)

    return ("", 404)

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


