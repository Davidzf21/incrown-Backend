from pickle import TRUE
from django.test import TestCase
import requests

url_prueba = 'http://127.0.0.1:8000/incrown_app/'
url_web = 'https://incrown.onrender.com/incrown_app/'

numPruebas = 0
numExitoPruebas = 0

def incrementar_numPruebas():
    global numPruebas
    numPruebas = numPruebas + 1
def incrementar_numExitoPruebas():
    global numExitoPruebas
    numExitoPruebas = numExitoPruebas + 1

# TEST USUARIOS
def test_usuarios(url):
    print("-----------------------------------------------------\nTEST: USUARIOS")
    requests.get(url + 'DeleteAll')
    #Creacion Buena
    auth_data = {'nombre': 'prueba', 'username': 'prueba', 'correo': 'prueba@gmail.com', 'password': '1234'}
    requests.post(url + 'CreateUsuario/', data=auth_data)
    incrementar_numPruebas()
    resp = requests.get(url + 'Usuario/prueba')
    t = resp.json()
    if "prueba" in t['username']:
        incrementar_numExitoPruebas()
        print("\t -> CREACION DE UN USUARIO --> FUNCIONA")
    else:
        print("\t -> CREACION DE UN USUARIO --> NO FUNCIONA")
    #Creacion Mala
    incrementar_numPruebas()
    auth_data = {'nombre': 'prueba', 'username': 'prueba', 'correo': 'prueba@gmail.com', 'password': '1234'}
    resp = requests.post(url + 'CreateUsuario/', data=auth_data)
    t = resp.json()
    if "Username ya existe" in t['message']:
        incrementar_numExitoPruebas()
        print("\t -> NO CREACION DE UN USUARIO YA EXISTENTE--> FUNCIONA")
    else:
        print("\t -> NO CREACION DE UN USUARIO YA EXISTENTE --> NO FUNCIONA")
    # Modificacion Buena
    incrementar_numPruebas()
    auth_data = {'nombre': 'prueba1', 'username': 'prueba', 'correo': 'prueba1@gmail.com', 'password': '12345'}
    requests.post(url + 'UpdateUsuario/prueba/', data=auth_data)
    resp = requests.get(url + 'Usuario/prueba')
    t = resp.json()
    if ("prueba1" in t['nombre']) & ("prueba1@gmail.com" in t['correo']):
        incrementar_numExitoPruebas()
        print("\t -> MODIFICACION DE UN USUARIO --> FUNCIONA")
    else:
        print("\t -> MODIFICACION DE UN USUARIO --> NO FUNCIONA")
    # Modificacion Mala
    incrementar_numPruebas()
    auth_data = {'nombre': 'prueba1', 'username': 'prueba', 'correo': 'prueba1@gmail.com', 'password': '12345'}
    resp = requests.post(url + 'UpdateUsuario/prueba1/', data=auth_data)
    t = resp.json()
    if ("Username no existe" in t['message']):
        incrementar_numExitoPruebas()
        print("\t -> NO MODIFICACION DE UN USUARIO NO EXISTENTE --> FUNCIONA")
    else:
        print("\t -> NO MODIFICACION DE UN USUARIO NO EXISTENTE --> NO FUNCIONA")
    # Login con contraseña Correcta
    incrementar_numPruebas()
    resp = requests.get(url + 'Login/prueba/12345')
    t = resp.json()
    if ("Contraseña correcta" in t['message']):
        incrementar_numExitoPruebas()
        print("\t -> LOGIN DE CONTRASEÑA CORRECTA --> FUNCIONA")
    else:
        print("\t -> LOGIN DE CONTRASEÑA CORRECTA --> NO FUNCIONA")
    # Login con contraseña Incorrecta
    incrementar_numPruebas()
    resp = requests.get(url + 'Login/prueba/123455')
    t = resp.json()
    if ("ERROR: Contraseña incorrecta" in t['message']):
        incrementar_numExitoPruebas()
        print("\t -> LOGIN DE CONTRASEÑA INCORRECTA --> FUNCIONA")
    else:
        print("\t -> LOGIN DE CONTRASEÑA INCORRECTA --> NO FUNCIONA")
    # Eliminacion Buena
    incrementar_numPruebas()
    resp = requests.get(url + 'DeleteUsuario/prueba')
    t = resp.json()
    if "Usuario eliminado" in t['message']:
        incrementar_numExitoPruebas()
        print("\t -> ELIMINACION DE UN USUARIO --> FUNCIONA")
    else:
        print("\t -> ELIMINACION DE UN USUARIO --> NO FUNCIONA")
    # Eliminacion Mala
    incrementar_numPruebas()
    resp = requests.get(url + 'DeleteUsuario/prueba1')
    t = resp.json()
    if "Username no existe" in t['message']:
        incrementar_numExitoPruebas()
        print("\t -> ELIMINACION DE UN USUARIO NO EXISTENTE --> FUNCIONA")
    else:
        print("\t -> ELIMINACION DE UN USUARIO NO EXISTENTE --> NO FUNCIONA")
    print("-----------------------------------------------------\n")

# TEST EVENTOS
def test_eventos(url):
    print("-----------------------------------------------------\nTEST: EVENTOS")
    # Creacion Buena
    incrementar_numPruebas()
    auth_data_us = {'nombre': 'evento_prueba', 'username': 'evento_prueba', 'correo': 'prueba@gmail.com', 
        'password': '1234'}
    requests.post(url + 'CreateUsuario/', data=auth_data_us)
    auth_data_ev = {'nombre': 'evento_prueba', 'descripcion': 'evento_prueba', 'fecha': '12/12/12', 
        'hora': '12', 'aforo': 12, 'categoria': 'evento_prueba', 'organizador': 'evento_prueba'}
    requests.post(url + 'CreateEvento/', data=auth_data_ev)
    resp = requests.get(url + 'Evento/evento_prueba')
    t = resp.json()
    if "evento_prueba" in t['nombre']:
        incrementar_numExitoPruebas()
        print("\t -> CREACION DE UN EVENTO --> FUNCIONA")
    else:
        print("\t -> CREACION DE UN EVENTO --> NO FUNCIONA")
    # Creacion Mala
    incrementar_numPruebas()
    resp = requests.post(url + 'CreateEvento/', data=auth_data_ev)
    t = resp.json()
    if "Ya existe un evento con ese nombre" in t['message']:
        incrementar_numExitoPruebas()
        print("\t -> NO CREACION DE UN EVENTO YA EXISTENTE --> FUNCIONA")
    else:
        print("\t -> NO CREACION DE UN EVENTO YA EXISTENTE --> NO FUNCIONA")
    # Modificacion Buena
    incrementar_numPruebas()
    auth_data_ev = {'nombre': 'evento_prueba', 'descripcion': 'evento_prueba1', 'fecha': '13/12/12', 
        'hora': '13', 'aforo': 13, 'categoria': 'evento_prueba1', 'organizador': 'evento_prueba'}
    resp = requests.put(url + 'UpdateEvento/evento_prueba/', data=auth_data_ev)
    resp = requests.get(url + 'Evento/evento_prueba')
    t = resp.json()
    if ("evento_prueba1" in t['descripcion']) & ("13/12/12" in t['fecha']) & ("13" in t['hora']) & ("evento_prueba1" in t['categoria']):
        incrementar_numExitoPruebas()
        print("\t -> MODIFICACION DE UN EVENTO--> FUNCIONA")
    else:
        print("\t -> MODIFICACION DE UN EVENTO --> NO FUNCIONA")
    # Eliminacion Buena
    incrementar_numPruebas()
    requests.delete(url + 'DeleteEvento/evento_prueba')
    resp = requests.get(url + 'Evento/evento_prueba')
    t = resp.json()
    if "Not found." in t['detail']:
        incrementar_numExitoPruebas()
        print("\t -> ELIMINACION DE UN USUARIO --> FUNCIONA")
    else:
        print("\t -> ELIMINACION DE UN USUARIO --> NO FUNCIONA")
    requests.delete(url + 'DeleteUsuario/evento_prueba')
    # Eliminacion Mala
    incrementar_numPruebas()
    resp = requests.delete(url + 'DeleteEvento/evento_prueba2')
    t = resp.json()
    if "Not found." in t['detail']:
        incrementar_numExitoPruebas()
        print("\t -> ELIMINACION DE UN USUARIO NO EXISTENTE --> FUNCIONA")
    else:
        print("\t -> ELIMINACION DE UN USUARIO NO EXISTENTE --> NO FUNCIONA")
    requests.delete(url + 'DeleteUsuario/evento_prueba')
    requests.get(url + 'DeleteAll')
    print("-----------------------------------------------------\n")

# TEST PARTICIPANTES
def test_participantes(url):
    print("-----------------------------------------------------\nTEST: PARTICIPANTES")
    auth_data_us = {'nombre': 'user_prueba', 'username': 'user_prueba', 'correo': 'prueba@gmail.com', 
        'password': '1234'}
    requests.post(url + 'CreateUsuario/', data=auth_data_us)
    auth_data_us = {'nombre': 'user_prueba', 'username': 'user_prueba1', 'correo': 'prueba1@gmail.com', 
        'password': '1234'}
    requests.post(url + 'CreateUsuario/', data=auth_data_us)
    auth_data_ev = {'nombre': 'evento_prueba', 'descripcion': 'evento_prueba', 'fecha': '12/12/12', 
        'hora': '12', 'aforo': 12, 'categoria': 'evento_prueba', 'organizador': 'user_prueba'}
    requests.post(url + 'CreateEvento/', data=auth_data_ev)
    # AÑADIR PARTICIPANTE BIEN
    incrementar_numPruebas()
    resp = requests.get(url + 'anadirParticipante/evento_prueba/user_prueba/')
    t = resp.json()
    if "correctamente" in t['message']:
        incrementar_numExitoPruebas()
        print("\t -> AÑADIR PARTICIPANTE --> FUNCIONA")
    else:
        print("\t -> AÑADIR PARTICIPANTE --> NO FUNCIONA")
    # AÑADIR PARTICIPANTE, NO EXISTE USUAIRO
    incrementar_numPruebas()
    resp = requests.get(url + 'anadirParticipante/evento_prueba/user_prueba2/')
    t = resp.json()
    if "ERROR: No existe el usuario" in t['message']:
        incrementar_numExitoPruebas()
        print("\t\t -> NO AÑADIR PARTICIPANTE, NO EXISTE USUARIO --> FUNCIONA")
    else:
        print("\t\t -> NO AÑADIR PARTICIPANTE, NO EXISTE USUARIO --> NO FUNCIONA")
    # AÑADIR PARTICIPANTE, NO EXISTE EVENTO
    incrementar_numPruebas()
    resp = requests.get(url + 'anadirParticipante/evento_prueba1/user_prueba/')
    t = resp.json()
    if "ERROR: No existe el evento" in t['message']:
        incrementar_numExitoPruebas()
        print("\t\t -> NO AÑADIR PARTICIPANTE, NO EXISTE EVENTO --> FUNCIONA")
    else:
        print("\t\t -> NO AÑADIR PARTICIPANTE, NO EXISTE EVENTO --> NO FUNCIONA")
    # AÑADIR PARTICIPANTE, YA ES PARTICIPANTE
    incrementar_numPruebas()
    resp = requests.get(url + 'anadirParticipante/evento_prueba/user_prueba/')
    t = resp.json()
    if "ERROR: No se ha introducido o el usuario ya es participante" in t['message']:
        incrementar_numExitoPruebas()
        print("\t\t -> NO AÑADIR PARTICIPANTE, YA ES PARTICIPANTE --> FUNCIONA")
    else:
        print("\t\t -> NO AÑADIR PARTICIPANTE, YA ES PARTICIPANTE --> NO FUNCIONA")
    # COMPROBAR PARTICIPANTE
    incrementar_numPruebas()
    resp = requests.get(url + 'esParticipante/evento_prueba/user_prueba/')
    t = resp.json()
    if "TRUE" in t['message']:
        incrementar_numExitoPruebas()
        print("\t -> COMPROBAR PARTICIPANTE, ES PARTICIPANTE --> FUNCIONA")
    else:
        print("\t -> COMPROBAR PARTICIPANTE, ES PARTICIPANTE --> NO FUNCIONA")
    # COMPROBAR PARTICIPANTE, NO ES PARTICIPANTE
    incrementar_numPruebas()
    resp = requests.get(url + 'esParticipante/evento_prueba/user_prueba1/')
    t = resp.json()
    if "FALSE" in t['message']:
        incrementar_numExitoPruebas()
        print("\t\t -> COMPROBAR PARTICIPANTE, NO ES PARTICIPANTE --> FUNCIONA")
    else:
        print("\t\t -> COMPROBAR PARTICIPANTE, NO ES PARTICIPANTE --> NO FUNCIONA")
    # COMPROBAR PARTICIPANTE, NO EXITE EL USUARIO
    incrementar_numPruebas()
    resp = requests.get(url + 'esParticipante/evento_prueba/user_prueba2/')
    t = resp.json()
    if "ERROR: No existe el usuario" in t['message']:
        incrementar_numExitoPruebas()
        print("\t\t -> COMPROBAR PARTICIPANTE, NO EXISTE USUARIO --> FUNCIONA")
    else:
        print("\t\t -> COMPROBAR PARTICIPANTE, NO EXISTE USUARIO --> NO FUNCIONA")
    # COMPROBAR PARTICIPANTE, NO EXISTE EVENTO
    incrementar_numPruebas()
    resp = requests.get(url + 'esParticipante/evento_prueba1/user_prueba/')
    t = resp.json()
    if "ERROR: No existe el evento" in t['message']:
        incrementar_numExitoPruebas()
        print("\t\t -> COMPROBAR PARTICIPANTE, NO EXISTE EVENTO --> FUNCIONA")
    else:
        print("\t\t -> COMPROBAR PARTICIPANTE, NO EXISTE EVENTO --> NO FUNCIONA")
    # ELIMINAR PARTICIPANTE
    incrementar_numPruebas()
    resp = requests.get(url + 'deleteParticipante/evento_prueba/user_prueba/')
    t = resp.json()
    if "correctamente" in t['message']:
        incrementar_numExitoPruebas()
        print("\t -> ELIMINAR PARTICIPANTE --> FUNCIONA")
    else:
        print("\t -> ELIMINAR PARTICIPANTE --> NO FUNCIONA")
    # ELIMINAR PARTICIPANTE, NO ERA PARTICIPANTE
    incrementar_numPruebas()
    resp = requests.get(url + 'deleteParticipante/evento_prueba/user_prueba1/')
    t = resp.json()
    if "ERROR: No se ha borrado o no era participente del evento" in t['message']:
        incrementar_numExitoPruebas()
        print("\t\t -> ELIMINAR PARTICIPANTE, NO ERA PARTICIPANTE --> FUNCIONA")
    else:
        print("\t\t -> ELIMINAR PARTICIPANTE, NO ERA PARTICIPANTE --> NO FUNCIONA")
    # ELIMINAR PARTICIPANTE, NO EXITE EL USUARIO
    incrementar_numPruebas()
    resp = requests.get(url + 'deleteParticipante/evento_prueba/user_prueba2/')
    t = resp.json()
    if "ERROR: No existe el usuario" in t['message']:
        incrementar_numExitoPruebas()
        print("\t\t -> ELIMINAR PARTICIPANTE, NO EXISTE USUARIO --> FUNCIONA")
    else:
        print("\t\t -> ELIMINAR PARTICIPANTE, NO EXISTE USUARIO --> NO FUNCIONA")
    # ELIMINAR PARTICIPANTE, NO EXISTE EVENTO
    incrementar_numPruebas()
    resp = requests.get(url + 'deleteParticipante/evento_prueba1/user_prueba/')
    t = resp.json()
    if "ERROR: No existe el evento" in t['message']:
        incrementar_numExitoPruebas()
        print("\t\t -> ELIMINAR PARTICIPANTE, NO EXISTE EVENTO --> FUNCIONA")
    else:
        print("\t\t -> ELIMINAR PARTICIPANTE, NO EXISTE EVENTO --> NO FUNCIONA")
    # EVENTOS EN LOS QUE PARTICIPA UN USUARIO
    incrementar_numPruebas()
    requests.get(url + 'anadirParticipante/evento_prueba/user_prueba/')
    resp = requests.get(url + 'eventosApuntados/user_prueba/')
    t = resp.json()
    if "evento_prueba" in t[0]['nombre']:
        incrementar_numExitoPruebas()
        print("\t -> EVENTOS EN LOS QUE PARTICIPA UN USUARIO --> FUNCIONA")
    else:
        print("\t -> EVENTOS EN LOS QUE PARTICIPA UN USUARIO --> NO FUNCIONA")
    # EVENTOS EN LOS QUE NO PARTICIPA UN USUARIO
    incrementar_numPruebas()
    resp = requests.get(url + 'eventosNoApuntados/user_prueba/')
    t = resp.json()
    if len(t) == 0:
        incrementar_numExitoPruebas()
        print("\t -> EVENTOS EN LOS QUE NO PARTICIPA UN USUARIO --> FUNCIONA")
    else:
        print("\t -> EVENTOS EN LOS QUE NO PARTICIPA UN USUARIO --> NO FUNCIONA")
    requests.get(url + 'DeleteAll')
    print("-----------------------------------------------------\n")

# TEST MENSAJES
def test_mensajes(url):
    print("-----------------------------------------------------\nTEST: MENSAJES")
    auth_data_us = {'nombre': 'user_prueba', 'username': 'user_prueba', 'correo': 'prueba@gmail.com', 
        'password': '1234'}
    requests.post(url + 'CreateUsuario/', data=auth_data_us)
    auth_data_ev = {'nombre': 'evento_prueba', 'descripcion': 'evento_prueba', 'fecha': '12/12/12', 
        'hora': '12', 'aforo': 12, 'categoria': 'evento_prueba', 'organizador': 'user_prueba'}
    requests.post(url + 'CreateEvento/', data=auth_data_ev)
    requests.get(url + 'anadirParticipante/evento_prueba/user_prueba/')
    mensaje_data_ev = {'autor': 'user_prueba', 'evento': 'evento_prueba', 'texto': 'mensaje1'}
    # CREAR MENSAJE
    incrementar_numPruebas()
    requests.post(url + 'CreateMensaje/', data=mensaje_data_ev)
    resp = requests.get(url + 'Mensajes/evento_prueba')
    t = resp.json()
    if ("user_prueba" in t[0]['autor']) & ("evento_prueba" in t[0]['evento']) & ("mensaje1" in t[0]['texto']):
        incrementar_numExitoPruebas()
        print("\t -> CREACION DE UN MENSAJE--> FUNCIONA")
    else:
        print("\t -> CREACION DE UN MENSAJE --> NO FUNCIONA")
    requests.get(url + 'DeleteAll')
    #Delete Mensaje
    incrementar_numPruebas()
    resp = requests.get(url + 'Mensajes/')
    t = resp.json()
    if len(t) == 0:
        incrementar_numExitoPruebas()
        print("\t -> MENSAJES BORRADOS CUANDO SE BORRA EL EVENTO --> FUNCIONA")
    else:
        print("\t -> MENSAJES BORRADOS CUANDO SE BORRA EL EVENTO --> NO FUNCIONA")
    requests.get(url + 'DeleteAll')
    print("-----------------------------------------------------\n") 

        
if __name__ == "__main__":
    pruebas = url_prueba
    test_usuarios(pruebas)
    test_eventos(pruebas)
    test_participantes(pruebas)
    test_mensajes(pruebas)
    print("Cobertura de las pruebas: "+str((numExitoPruebas/numPruebas)*100)+" %")
