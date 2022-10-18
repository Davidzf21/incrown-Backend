from webbrowser import get
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Usuario, Evento
from .serializers import UsuarioSerializer, EventoSerializer
from django.contrib.auth.hashers import make_password, check_password

#
# Funciones del USUARIO
#
class UsuarioCreate(generics.CreateAPIView):
   # API endpoint that allows creation of a new Usuario
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    def post(self, request, *args, **kwargs):
         response = {}
         us = Usuario.objects.filter(username=request.data['username'])
         if (us):
            # RESPONSE
            response['success'] = False
            response['message'] = "Username ya existe"
            response['status'] = status.HTTP_400_BAD_REQUEST
         else:
            nombre = request.data.get("nombre")
            username = request.data.get("username")
            correo = request.data.get("correo")
            pasword = make_password(request.data.get("password"))
            Usuario.objects.create(nombre=nombre,username=username,correo=correo, password=pasword)
            # RESPONSE
            response['success'] = True
            response['message'] = "Usuario creado exitosamente"
            response['status'] = status.HTTP_201_CREATED
         return Response(response)

class UsuarioUpdate(generics.RetrieveUpdateAPIView):
   queryset = Usuario.objects.all()
   lookup_field = 'username'
   serializer_class = UsuarioSerializer
   def put(self, request, *args, **kwargs):
      us = Usuario.objects.get(username=self.kwargs['username'])
      if request.data['password'] == us.password:
         return self.partial_update(request, *args, **kwargs)
      else:
         request.data._mutable = True
         request.data['password'] = make_password(request.data["password"])
         request.data._mutable = False
         return self.partial_update(request, *args, **kwargs) 

class UsuariosList(generics.ListAPIView):
   queryset = Usuario.objects.all()
   serializer_class = UsuarioSerializer

class UsuarioList(generics.RetrieveAPIView):
    lookup_field = 'username'
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioDelete(generics.RetrieveDestroyAPIView):
    # API endpoint that allows a Usuario record to be deleted
    queryset = Usuario.objects.all()
    lookup_field = 'username'
    serializer_class = UsuarioSerializer


#
# Funciones del EVENTO
#
class EventoCreate(generics.CreateAPIView):
    # API endpoint that allows creation of a new Evento
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    def post(self, request, *args, **kwargs):
      response = {}
      us = Usuario.objects.filter(username=request.data['organizador'])
      if(us):
         us = Usuario.objects.get(username=request.data['organizador'])
         us.numEventosCreados = us.numEventosCreados + 1
         us.save()
         self.create(request, *args, **kwargs)
         response['success'] = True
         response['message'] = "Evento creado exitosamente"
         response['status'] = status.HTTP_201_CREATED
         return Response(response)
      else:
         response['success'] = False
         response['message'] = "No existe un usuario organizador"
         response['status'] = status.HTTP_400_BAD_REQUEST
         return Response(response)

class EventosList(generics.ListAPIView):
   queryset = Evento.objects.all()
   serializer_class = EventoSerializer

class EventoList(generics.RetrieveAPIView):
    lookup_field = 'nombre'
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

class EventoUpdate(generics.RetrieveUpdateAPIView):
   # API endpoint that allows a Evento record to be updated.
   queryset = Evento.objects.all()
   lookup_field = 'nombre'
   serializer_class = EventoSerializer
   def put(self, request, *args, **kwargs):
      return self.partial_update(request, *args, **kwargs)

class EventoDelete(generics.RetrieveDestroyAPIView):
   # API endpoint that allows a Evento record to be deleted.
   queryset = Evento.objects.all()
   lookup_field = 'nombre'
   serializer_class = EventoSerializer