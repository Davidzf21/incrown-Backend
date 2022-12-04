from webbrowser import get
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Usuario, Evento, Mensaje
from .serializers import EventoSerializerAll, UsuarioSerializer, EventoSerializer, MensajeSerializer
from django.contrib.auth.hashers import make_password, check_password
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import string, random

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

class UsuarioUpdate(generics.ListAPIView):
   # API endpoint that allows creation of a new Usuario
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    def post(self, request, *args, **kwargs):
         response = {}
         us = Usuario.objects.filter(username=self.kwargs['username'])
         if (us):
            us = Usuario.objects.get(username=self.kwargs['username'])
            us.nombre = request.data.get("nombre")
            us.username = request.data.get("username")
            us.correo = request.data.get("correo")
            us.pasword = make_password(request.data.get("password"))
            us.save()
            #Usuario.objects.update(nombre=nombre,username=username,correo=correo, password=pasword)
            # RESPONSE
            response['success'] = True
            response['message'] = "Usuario modificado exitosamente"
            response['status'] = status.HTTP_201_CREATED
         else:
            # RESPONSE
            response['success'] = False
            response['message'] = "Username no existe"
            response['status'] = status.HTTP_400_BAD_REQUEST
         return Response(response)

class UsuariosList(generics.ListAPIView):
   queryset = Usuario.objects.all()
   serializer_class = UsuarioSerializer

class UsuarioList(generics.RetrieveAPIView):
    lookup_field = 'username'
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioDelete(generics.ListAPIView):
   queryset = Usuario.objects.all()
   serializer_class = UsuarioSerializer

   def list(self, request, *args, **kwargs):
      nomUsuario=self.kwargs['username']
      response = {}
      usuario = Usuario.objects.filter(username=nomUsuario)
      if(usuario):
         usuario = Usuario.objects.get(username=nomUsuario)
         beforeDelete = Usuario.objects.count()
         usuario.delete()
         afterDelete = Usuario.objects.count()
         if  beforeDelete == afterDelete:
            # RESPONSE
            response['success'] = False
            response['message'] = "ERROR: No se han podido eliminar el usuario"
            response['status'] = status.HTTP_400_BAD_REQUEST
         else:
            # RESPONSE
            response['success'] = True
            response['message'] = "Usuario eliminado"
            response['status'] = status.HTTP_200_OK
      else:
            # RESPONSE
            response['success'] = False
            response['message'] = "Username no existe"
            response['status'] = status.HTTP_400_BAD_REQUEST
      return Response(response)

class UsuarioDeleteAll(generics.ListAPIView):
   queryset = Usuario.objects.all()
   serializer_class = UsuarioSerializer

   def list(self, request, *args, **kwargs):
      response = {}
      Usuario.objects.all().delete()
      n = Usuario.objects.count()
      if  n == 0:
         # RESPONSE
         response['success'] = True
         response['message'] = "Borrado todos los usuarios"
         response['status'] = status.HTTP_200_OK
      else:
         # RESPONSE
         response['success'] = False
         response['message'] = "ERROR: No se han podido eliminar todos los usuarios"
         response['status'] = status.HTTP_400_BAD_REQUEST
      return Response(response)

class Login(generics.ListAPIView):
   queryset = Usuario.objects.all()
   serializer_class = UsuarioSerializer
   def list(self, request, *args, **kwargs):
      response = {}
      us = Usuario.objects.filter(username=self.kwargs['username'])
      if(us):
         us = Usuario.objects.get(username=self.kwargs['username'])
         check = check_password(self.kwargs['contrasena'], us.password)
         if(check):
            response['success'] = True
            response['message'] = "Contraseña correcta"
            response['status'] = status.HTTP_200_OK
         else:
            response['success'] = False
            response['message'] = "ERROR: Contraseña incorrecta"
            response['status'] = status.HTTP_409_CONFLICT
      else:
         response['success'] = False
         response['message'] = "ERROR: EL usuario no existe"
         response['status'] = status.HTTP_409_CONFLICT
      return Response(response)

class ValorarUsuario(generics.RetrieveUpdateAPIView):
    # API endpoint that allows a Usuario record to be updated.
    queryset = Usuario.objects.all()
    lookup_field = 'username'
    serializer_class = UsuarioSerializer
    def put(self, request, *args, **kwargs):
        usuario = Usuario.objects.get(username=self.kwargs['username'])
        request.data['numValoraciones'] = usuario.numValoraciones + 1
        request.data['valoracion'] = ((usuario.valoracion*(usuario.numValoraciones))+request.data['valoracion'])/request.data['numValoraciones']
        return self.partial_update(request, *args, **kwargs)
      
class RecuperarContrasena(generics.RetrieveAPIView):
   queryset = Usuario.objects.all()
   serializer_class = UsuarioSerializer
   lookup_field = 'correo'

   def get(self, request, *args, **kwargs):
      
      response={}
      usuario = Usuario.objects.filter(correo=self.kwargs['correo'])
      if(usuario):
         # Generar una contraseña aleatoria nueva
         contrasena = ''
         length_of_string = 8
         for x in range(length_of_string):
            contrasena = contrasena + random.choice(string.ascii_letters)
         
         # Guardar la nueva contraseña en los datos del usuario
         usuario = Usuario.objects.get(correo=self.kwargs['correo'])
         usuario.password = make_password(contrasena)
         usuario.save()

         # Enviar la nueva contraseña al correo electronico del usuario
         email = self.kwargs['correo']
         contrasenya = str(contrasena)
         html = '<h1>Su contraseña es -> '+contrasenya+'</h1>'
         mail = MIMEMultipart('alternative')
         mail['From'] = 'univibesunizar1234@gmail.com'
         mail['To'] = email
         mail['Cc'] = ''
         mail['Subject'] = 'Su nueva contraseña es '+contrasenya
         part2 = MIMEText(html, 'html')
         mail.attach(part2)
         msg_full = mail.as_string().encode()
         server = smtplib.SMTP('smtp.gmail.com', 587)
         server.starttls()
         #Contraseña generada por Google para poder enviar correos -> njcncdvsswrmtzmw
         #Contraseña de la cuenta -> 1234univibesunizar
         server.login('univibesunizar1234@gmail.com', 'njcncdvsswrmtzmw')
         server.sendmail('univibesunizar1234@gmail.com', email, msg_full)
         server.quit()

         # RESPONSE
         response['success'] = True
         response['message'] = "Correo enviado correctamente"
         response['status'] = status.HTTP_200_OK
      else:
         # RESPONSE
         response['success'] = False
         response['message'] = "ERROR: No existe un usuario con el ese correo"
         response['status'] = status.HTTP_400_BAD_REQUEST
      return Response(response)
      

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
         else:
            us.numEventosCreados = us.numEventosCreados + 1
            us.save()
            self.create(request, *args, **kwargs)
            response['success'] = True
            response['message'] = "Evento creado exitosamente"
            response['status'] = status.HTTP_200_OK
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

class EventoDeleteAll(generics.ListAPIView):
   queryset = Evento.objects.all()
   serializer_class = EventoSerializer

   def list(self, request, *args, **kwargs):
      response = {}
      Evento.objects.all().delete()
      n = Evento.objects.count()
      if  n == 0:
         # RESPONSE
         response['success'] = True
         response['message'] = "Borrado todos los eventos"
         response['status'] = status.HTTP_200_OK
      else:
         # RESPONSE
         response['success'] = False
         response['message'] = "ERROR: No se han podido eliminar todos los eventos"
         response['status'] = status.HTTP_400_BAD_REQUEST
      return Response(response)

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
               else:
                  usuario.numEventosParticipa = usuario.numEventosParticipa + 1
                  response['success'] = True
                  response['message'] = "Se ha introducido correctamente"
                  response['status'] = status.HTTP_200_OK
            else:
               response['success'] = False
               response['message'] = "ERROR: No existe el usuario"
               response['status'] = status.HTTP_409_CONFLICT
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
            else:
               response['success'] = False
               response['message'] = "FALSE"
               response['status'] = status.HTTP_200_OK
         else:
            response['success'] = False
            response['message'] = "ERROR: No existe el evento"
            response['status'] = status.HTTP_409_CONFLICT
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
            else:
               usuario.numEventosParticipa = usuario.numEventosParticipa - 1
               response['success'] = True
               response['message'] = "Se ha borrado correctamente"
               response['status'] = status.HTTP_200_OK
         else:
            response['success'] = False
            response['message'] = "ERROR: No existe el usuario"
            response['status'] = status.HTTP_409_CONFLICT
      else:
         response['success'] = False
         response['message'] = "ERROR: No existe el evento"
         response['status'] = status.HTTP_409_CONFLICT
      return Response(response)

class eventosApuntados(generics.ListAPIView):
   queryset = Evento.objects.all()
   serializer_class = EventoSerializer

   def list(self, request, *args, **kwargs):
      nomUsuario=self.kwargs['nomUsuario']
      usuario = Usuario.objects.filter(username=nomUsuario)
      if(usuario):
         usuario = Usuario.objects.get(username=nomUsuario)
         queryset = Evento.objects.filter(participantes=usuario)
         page = self.paginate_queryset(queryset)
         if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
         else:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
      else:
         # RESPONSE
         response={}
         response['success'] = False
         response['message'] = "Username no existe"
         response['status'] = status.HTTP_400_BAD_REQUEST
         return Response(response)

class eventosNoApuntados(generics.ListAPIView):
   queryset = Evento.objects.all()
   serializer_class = EventoSerializer

   def list(self, request, *args, **kwargs):
      nomUsuario=self.kwargs['nomUsuario']
      usuario = Usuario.objects.filter(username=nomUsuario)
      if(usuario):
         usuario = Usuario.objects.get(username=nomUsuario)
         queryset = Evento.objects.exclude(participantes=usuario)
         page = self.paginate_queryset(queryset)
         if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
         serializer = self.get_serializer(queryset, many=True)
         return Response(serializer.data)
      else:
         # RESPONSE
         response={}
         response['success'] = False
         response['message'] = "Username no existe"
         response['status'] = status.HTTP_400_BAD_REQUEST
         return Response(response)


#
# AMIGOS
#
class anadirAmigo(generics.ListAPIView):
   queryset = Usuario.objects.all()
   serializer_class = UsuarioSerializer

   def list(self, request, *args, **kwargs):
      nomAmigo=self.kwargs['nomAmigo']
      nomUsuario=self.kwargs['nomUsuario']
      response = {}
      usuario = Usuario.objects.filter(username=nomUsuario)
      if(usuario):
         usuario = Usuario.objects.get(username=nomUsuario)
         amigo = Usuario.objects.filter(username=nomAmigo)
         if(amigo):
            amigo = Usuario.objects.get(username=nomAmigo)
            beforeInsert = Usuario.objects.filter(amigos=amigo).count()
            usuario.amigos.add(amigo)
            afterInsert = Usuario.objects.filter(amigos=amigo).count()
            if  beforeInsert == afterInsert:
               # RESPONSE
               response['success'] = False
               response['message'] = "ERROR: Ya son amigos estos usuarios"
               response['status'] = status.HTTP_400_BAD_REQUEST
            else:
               # RESPONSE
               response['success'] = True
               response['message'] = "Amigo añadido correctamente"
               response['status'] = status.HTTP_200_OK
         else:
            # RESPONSE
            response['success'] = False
            response['message'] = "Amigo no existe"
            response['status'] = status.HTTP_400_BAD_REQUEST
      else:
            # RESPONSE
            response['success'] = False
            response['message'] = "Username no existe"
            response['status'] = status.HTTP_400_BAD_REQUEST
      return Response(response)

class esAmigo(generics.ListAPIView):
   queryset = Usuario.objects.all()
   serializer_class = UsuarioSerializer

   def list(self, request, *args, **kwargs):
      nomUsuario=self.kwargs['nomUsuario']
      nomAmigo=self.kwargs['nomAmigo']
      response={}
      amigo = Usuario.objects.filter(username=nomAmigo)
      if(amigo):
         amigo = Usuario.objects.get(username=nomAmigo)
         num = Usuario.objects.filter(username=nomAmigo)
         if(num):
            num = Usuario.objects.filter(amigos=amigo)
            num = num.filter(username=nomUsuario)
            if  num:
               # RESPONSE
               response['success'] = True
               response['message'] = "Son amigos"
               response['status'] = status.HTTP_200_OK
            else:
               # RESPONSE
               response['success'] = False
               response['message'] = "No son amigos"
               response['status'] = status.HTTP_200_OK
         else:
            # RESPONSE
            response['success'] = False
            response['message'] = "Amigo no existe"
            response['status'] = status.HTTP_400_BAD_REQUEST
      else:
         # RESPONSE
         response['success'] = False
         response['message'] = "Username no existe"
         response['status'] = status.HTTP_400_BAD_REQUEST
      return Response(response)

class amigosUsuario(generics.ListAPIView):
   queryset = Usuario.objects.all()
   serializer_class = UsuarioSerializer

   def list(self, request, *args, **kwargs):
      nomUsuario=self.kwargs['nomUsuario']
      usuario = Usuario.objects.filter(username=nomUsuario)
      if(usuario):
         usuario = Usuario.objects.get(username=nomUsuario)
         queryset = usuario.amigos.all()
         page = self.paginate_queryset(queryset)
         if page is not None:
               serializer = self.get_serializer(page, many=True)
               return self.get_paginated_response(serializer.data)
         serializer = self.get_serializer(queryset, many=True)
         return Response(serializer.data)
      else:
         # RESPONSE
         response={}
         response['success'] = False
         response['message'] = "Username no existe"
         response['status'] = status.HTTP_400_BAD_REQUEST
         return Response(response)

class deleteAmigo(generics.ListAPIView):
   queryset = Usuario.objects.all()
   serializer_class = UsuarioSerializer

   def list(self, request, *args, **kwargs):
      nomAmigo=self.kwargs['nomAmigo']
      nomUsuario=self.kwargs['nomUsuario']
      response = {}
      usuario = Usuario.objects.filter(username=nomUsuario)
      if(usuario):
         usuario = Usuario.objects.get(username=nomUsuario)
         amigo = Usuario.objects.filter(username=nomAmigo)
         if(amigo):
            amigo = Usuario.objects.get(username=nomAmigo)
            beforeInsert = Usuario.objects.filter(amigos=amigo).count()
            usuario.amigos.remove(amigo)
            afterInsert = Usuario.objects.filter(amigos=amigo).count()
            if  beforeInsert == afterInsert:
               # RESPONSE
               response['success'] = False
               response['message'] = "ERROR: No eran amigos estos usuarios"
               response['status'] = status.HTTP_400_BAD_REQUEST
            else:
               # RESPONSE
               response['success'] = True
               response['message'] = "Amigo borrado correctamente"
               response['status'] = status.HTTP_200_OK
         else:
            # RESPONSE
            response['success'] = False
            response['message'] = "Amigo no existe"
            response['status'] = status.HTTP_400_BAD_REQUEST
      else:
            # RESPONSE
            response['success'] = False
            response['message'] = "Username no existe"
            response['status'] = status.HTTP_400_BAD_REQUEST
      return Response(response)


#
# MENSAJES
#
class createMensaje(generics.CreateAPIView):
   queryset = Mensaje.objects.all()
   serializer_class = MensajeSerializer

   def post(self, request, *args, **kwargs):
      response = {}
      us = Usuario.objects.filter(username=request.data['autor'])
      if(us):
         us = Usuario.objects.get(username=request.data['autor'])
         ev = Evento.objects.filter(nombre=request.data['evento'])
         if(ev):
            ev = Evento.objects.get(nombre=request.data['evento'])
            Mensaje.objects.create(autor=us,evento=ev,texto=request.data['texto'])
            response['success'] = True
            response['message'] = "Mensaje guardado exitosamente"
            response['status'] = status.HTTP_201_CREATED
         else:
            response['success'] = False
            response['message'] = "ERROR: No existe el evento"
            response['status'] = status.HTTP_409_CONFLICT
      else:
         response['success'] = False
         response['message'] = "ERROR: No existe el usuario"
         response['status'] = status.HTTP_409_CONFLICT
      return Response(response)

class listMensajes(generics.ListAPIView):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer

class listMensajeEventos(generics.ListAPIView):
   queryset = Mensaje.objects.all()
   serializer_class = MensajeSerializer

   def get_queryset(self):
      nomEvento=self.kwargs['nomEvento']
      evento_id = Evento.objects.get(nombre=nomEvento)
      return Mensaje.objects.filter(evento=evento_id)

class DeleteAll(generics.ListAPIView):
   queryset = Evento.objects.all()
   serializer_class = EventoSerializer

   def list(self, request, *args, **kwargs):
      response = {}
      Evento.objects.all().delete()
      Usuario.objects.all().delete()
      ne = Evento.objects.count()
      nu = Usuario.objects.count()
      if  ne != 0:
         # RESPONSE
         response['success'] = False
         response['message'] = "ERROR: No se han borrado todos los eventos"
         response['status'] = status.HTTP_200_OK
      elif nu != 0:
         # RESPONSE
         response['success'] = False
         response['message'] = "ERROR: No se han borrado todos los usuarios"
         response['status'] = status.HTTP_400_BAD_REQUEST
      else:
         # RESPONSE
         response['success'] = True
         response['message'] = "Se han borrado todos los datos del sistema"
         response['status'] = status.HTTP_200_OK
      return Response(response)