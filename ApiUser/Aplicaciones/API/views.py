from django.shortcuts import render
from django.views import View
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
import json

from django.contrib.auth.models import User

class userView(View):
#********************Decorador para omitir el CSRF***********
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
#**********************************************************  

    def post(self,request):
        jd = json.loads(request.body)
        usuario = jd['usuario']
        contraseña = jd['contraseña']
        session = SessionStore()
        session['username'] = usuario
        session = request.session
        session['my_key'] = 'my_value'
        session.save()
        user = authenticate(request, username=usuario, password=contraseña)
        if user is not None and user.check_password(contraseña):
            login(request,user)
            data = {"message": "Usuario correcto",
                    "session_id": session.session_key,
                    "username":usuario,
                    "is_logged_in": True}
        else:
            data = {"message": "Usuario o contraseña incorrectos","is_logged_in": False}
        return JsonResponse(data)

    
    def get(self,request):

        session = SessionStore(session_key=request.COOKIES.get('session_id'))
        username = session.get('_auth_user_id')
        if username:
            user = User.objects.get(pk=username)
            data = {'message': 'Usuario correcto', 'username': user.username, 'is_logged_in': True}   

        else:
            data = {'message': 'No hay usuarios logueados', 'is_logged_in': False}
        return JsonResponse(data)

    def delete(self,request):
        session = SessionStore(session_key=request.COOKIES.get('session_id'))
        session.flush()
        data = {'message':'Usuario deslogueado','is_logged_in':False}
        response = JsonResponse(data)
        response.delete_cookie('session_id')
        return response
