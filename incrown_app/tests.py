from pickle import TRUE
from django.test import TestCase
import requests
#from models import Usuario

# Create your tests here.
#factory = APIRequestFactory()
#request = factory.post('/notes/', {'title': 'new idea'})

url_prueba = 'http://127.0.0.1:8000/incrown_app/'
url_web = 'https://incrown.onrender.com/incrown_app/'

# TEST USUARIOS
def test_usuarios(url):
    print("----------------\nTEST: USUARIOS")
    #Creacion
    auth_data = {'nombre': 'prueba', 'username': 'prueba', 'correo': 'prueba@gmail.com', 'password': '1234'}
    requests.post(url + 'CreateUsuario/', data=auth_data)
    resp = requests.get(url + 'Usuario/prueba')
    t = resp.json()
    if "prueba" in t['username']:
        print("\t -> CREACION DE UN USUARIO --> FUNCIONA")
    else:
        print("\t -> CREACION DE UN USUARIO --> NO FUNCIONA")
    #Modificacion
    auth_data = {'nombre': 'prueba1', 'username': 'prueba', 'correo': 'prueba1@gmail.com', 'password': '12345'}
    requests.put(url + 'UpdateUsuario/prueba/', data=auth_data)
    resp = requests.get(url + 'Usuario/prueba')
    t = resp.json()
    if ("prueba1" in t['nombre']) & ("prueba1@gmail.com" in t['correo']):
        print("\t -> MODIFICACION DE UN USUARIO --> FUNCIONA")
    else:
        print("\t -> MODIFICACION DE UN USUARIO --> NO FUNCIONA")
    #Eliminacion
    requests.delete(url + 'DeleteUsuario/prueba')
    resp = requests.get(url + 'Usuario/prueba')
    t = resp.json()
    if "Not found." in t['detail']:
        print("\t -> ELIMINACION DE UN USUARIO --> FUNCIONA")
    else:
        print("\t -> ELIMINACION DE UN USUARIO --> NO FUNCIONA")
    print("----------------\n")

# TEST EVENTOS
def test_eventos(url):
    print("----------------\nTEST: EVENTOS")
    #Creacion
    auth_data_us = {'nombre': 'evento_prueba', 'username': 'evento_prueba', 'correo': 'prueba@gmail.com', 
        'password': '1234'}
    requests.post(url + 'CreateUsuario/', data=auth_data_us)
    auth_data_ev = {'nombre': 'evento_prueba', 'descripcion': 'evento_prueba', 'fecha': '12/12/12', 
        'hora': '12', 'esPublico': TRUE, 'aforo': 12, 'categoria': 'evento_prueba', 'organizador': 'evento_prueba'}
    resp = requests.post(url + 'CreateEvento/', data=auth_data_ev)
    print(resp)
    #resp = requests.get(url + 'Evento/evento_prueba')
    #t = resp.json()
    #print(t)
    #if "evento_prueba" in t['nombre']:
    #    print("\t -> CREACION DE UN EVENTO --> FUNCIONA")
    #else:
    #    print("\t -> CREACION DE UN EVENTO --> NO FUNCIONA")
    #Modificacion
    #auth_data = {'nombre': 'prueba1', 'username': 'prueba', 'correo': 'prueba1@gmail.com', 'password': '12345'}
    #requests.put(url + 'UpdateUsuario/prueba/', data=auth_data)
    #resp = requests.get(url + 'Usuario/prueba')
    #t = resp.json()
    #if ("prueba1" in t['nombre']) & ("prueba1@gmail.com" in t['correo']):
    #    print("\t -> MODIFICACION DE UN USUARIO --> FUNCIONA")
    #else:
    #    print("\t -> MODIFICACION DE UN USUARIO --> NO FUNCIONA")
    #Eliminacion
    #requests.delete(url + 'DeleteUsuario/prueba')
    #resp = requests.get(url + 'Usuario/prueba')
    #t = resp.json()
    #if "Not found." in t['detail']:
    #    print("\t -> ELIMINACION DE UN USUARIO --> FUNCIONA")
    #else:
    #    print("\t -> ELIMINACION DE UN USUARIO --> NO FUNCIONA")
    #print("----------------\n")

if __name__ == "__main__":
    pruebas = url_prueba
    #test_usuarios(pruebas)
    test_eventos(pruebas)
