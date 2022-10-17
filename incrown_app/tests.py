from pickle import TRUE
from django.test import TestCase
from pyparsing import And
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

if __name__ == "__main__":
    test_usuarios(url_prueba)
