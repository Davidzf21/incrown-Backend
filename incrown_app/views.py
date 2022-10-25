from webbrowser import get
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Usuario, Evento
from .serializers import EventoSerializerAll, UsuarioSerializer, EventoSerializer
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
         ev = Evento.objects.filter(nombre=request.data['nombre'])
         if(ev):
            response['success'] = False
            response['message'] = "Ya existe un evento con ese nombre"
            response['status'] = status.HTTP_409_CONFLICT
            return Response(response)
         else:
            us.numEventosCreados = us.numEventosCreados + 1
            us.save()
            self.create(request, *args, **kwargs)
            response['success'] = True
            response['message'] = "Evento creado exitosamente"
            response['status'] = status.HTTP_200_OK
            return Response(response)
      else:
         response['success'] = False
         response['message'] = "No existe un usuario organizador"
         response['status'] = status.HTTP_409_CONFLICT
         return Response(response)

class EventosList(generics.ListAPIView):
   queryset = Evento.objects.all()
   serializer_class = EventoSerializer

class EventoList(generics.RetrieveAPIView):
    lookup_field = 'nombre'
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

class EventoListUsuario(generics.ListAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset((self.get_queryset()).filter(organizador=self.kwargs['username']))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

class EventoListAll(generics.ListAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializerAll

class EventoUpdate(generics.RetrieveUpdateAPIView):
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


#
# PARTICIANTES
#
class anadirParticipante(generics.ListAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    def list(self, request, *args, **kwargs):
         response = {}
         nomEvento=self.kwargs['nomEvento']
         nomUsuario=self.kwargs['nomUsuario']
         ev = Evento.objects.filter(nombre=nomEvento)
         if ev:
            evento = Evento.objects.get(nombre=nomEvento)
            us = Usuario.objects.filter(username=nomUsuario)
            if us:
               usuario = Usuario.objects.get(username=nomUsuario)
               beforeInsert = Evento.objects.filter(participantes=usuario).count()
               evento.participantes.add(usuario)
               afterInsert = Evento.objects.filter(participantes=usuario).count()
               if  beforeInsert == afterInsert:
                  response['success'] = False
                  response['message'] = "ERROR: No se ha introducido o el usuario ya es participante"
                  response['status'] = status.HTTP_409_CONFLICT
                  return Response(response)
               else:
                  usuario.numEventosParticipa = usuario.numEventosParticipa + 1
                  response['success'] = True
                  response['message'] = "Se ha introducido correctamente"
                  response['status'] = status.HTTP_200_OK
                  return Response(response)
            else:
               response['success'] = False
               response['message'] = "ERROR: No existe el usuario"
               response['status'] = status.HTTP_409_CONFLICT
               return Response(response)
         else:
            response['success'] = False
            response['message'] = "ERROR: No existe el evento"
            response['status'] = status.HTTP_409_CONFLICT
            return Response(response)

class esParticipante(generics.ListAPIView):
   queryset = Usuario.objects.all()
   serializer_class = UsuarioSerializer
   def list(self, request, *args, **kwargs):
      response = {}
      nomEvento=self.kwargs['nomEvento']
      nomUsuario=self.kwargs['nomUsuario']
      us = Usuario.objects.filter(username=nomUsuario)
      if us:
         usuario = Usuario.objects.get(username=nomUsuario)
         num = Evento.objects.filter(nombre=nomEvento)
         if num:
            num = Evento.objects.filter(participantes=usuario)
            num = num.filter(nombre=nomEvento)
            if num:
               response['success'] = True
               response['message'] = "TRUE"
               response['status'] = status.HTTP_200_OK
               return Response(response)
            else:
               response['success'] = False
               response['message'] = "FALSE"
               response['status'] = status.HTTP_200_OK
               return Response(response)
         else:
            response['success'] = False
            response['message'] = "ERROR: No existe el evento"
            response['status'] = status.HTTP_409_CONFLICT
            return Response(response)
      else:
         response['success'] = False
         response['message'] = "ERROR: No existe el usuario"
         response['status'] = status.HTTP_409_CONFLICT
         return Response(response)

class eliminarParticipante(generics.ListAPIView):
   queryset = Evento.objects.all()
   serializer_class = EventoSerializer
   def list(self, request, *args, **kwargs):
      response = {}
      nomEvento=self.kwargs['nomEvento']
      nomUsuario=self.kwargs['nomUsuario']
      ev = Evento.objects.filter(nombre=nomEvento)
      if ev:
         evento = Evento.objects.get(nombre=nomEvento)
         us = Usuario.objects.filter(username=nomUsuario)
         if us:
            usuario = Usuario.objects.get(username=nomUsuario)
            beforeInsert = Evento.objects.filter(participantes=usuario).count()
            evento.participantes.remove(usuario)
            afterInsert = Evento.objects.filter(participantes=usuario).count()
            if  beforeInsert <= afterInsert:
               response['success'] = False
               response['message'] = "ERROR: No se ha borrado o no era participente del evento"
               response['status'] = status.HTTP_409_CONFLICT
               return Response(response)
            else:
               usuario.numEventosParticipa = usuario.numEventosParticipa - 1
               response['success'] = True
               response['message'] = "Se ha borrado correctamente"
               response['status'] = status.HTTP_200_OK
               return Response(response)
         else:
            response['success'] = False
            response['message'] = "ERROR: No existe el usuario"
            response['status'] = status.HTTP_409_CONFLICT
            return Response(response)
      else:
         response['success'] = False
         response['message'] = "ERROR: No existe el evento"
         response['status'] = status.HTTP_409_CONFLICT
         return Response(response)