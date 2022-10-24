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
                  return Response({'message': 'ERROR: No se ha introducido o el usuario ya es participante'}, status=status.HTTP_409_CONFLICT)
               else:
                  usuario.numEventosParticipa = usuario.numEventosParticipa + 1
                  return Response({'message': 'Se ha introducido correctamente'}, status=status.HTTP_200_OK)
            else:
               return Response({'message': 'ERROR: No existe el usuario'}, status=status.HTTP_409_CONFLICT)
         else:
            return Response({'message': 'ERROR: No existe el evento'}, status=status.HTTP_409_CONFLICT)

class esParticipante(generics.ListAPIView):
   queryset = Usuario.objects.all()
   serializer_class = UsuarioSerializer
   def list(self, request, *args, **kwargs):
      nomEvento=self.kwargs['nomEvento']
      nomUsuario=self.kwargs['nomUsuario']
      us = Usuario.objects.filter(username=nomUsuario)
      if us:
         usuario = Usuario.objects.get(username=nomUsuario)
         num = Evento.objects.filter(nombre=nomEvento)
         if num:
            num = Evento.objects.filter(participantes=usuario)
            num = num.filter(nombre=nomEvento)
            if  num:
               return Response({'message': 'TRUE'}, status=status.HTTP_200_OK)
            else:
               return Response({'message': 'FALSE'}, status=status.HTTP_200_OK)
         else:
            return Response({'message': 'No existe el evento'}, status=status.HTTP_409_CONFLICT)
      else:
         return Response({'message': 'No existe el usuario'}, status=status.HTTP_409_CONFLICT)

class eliminarParticipante(generics.ListAPIView):
   queryset = Evento.objects.all()
   serializer_class = EventoSerializer
   def list(self, request, *args, **kwargs):
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
               return Response({'message': 'ERROR: No se ha borrado o no era participente del evento'}, status=status.HTTP_409_CONFLICT)
            else:
               usuario.numEventosParticipa = usuario.numEventosParticipa - 1
               return Response({'message': 'Se ha borrado correctamente'}, status=status.HTTP_200_OK)
         else:
            return Response({'message': 'ERROR: No existe el usuario'}, status=status.HTTP_409_CONFLICT)
      else:
         return Response({'message': 'ERROR: No existe el evento'}, status=status.HTTP_409_CONFLICT)