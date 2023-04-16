from django.shortcuts import render
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
import json




@method_decorator(csrf_exempt)
@api_view(['POST'])
def iniciarSesion(request):
    jd = json.loads(request.body)
    usuario = jd['usuario']
    password = jd['contraseña']
    
    user = authenticate(request, username=usuario, password=password)
    if user is not None and user.check_password(password):
        tok, created = Token.objects.get_or_create(user=user)
        token = tok.key
        login(request,user)
        data = {"message": "Usuario correcto",
                "token": token,
                "username": usuario,
                "is_logged_in": True}
        print(token)
        response = JsonResponse(data)
    else:
        data = {"message": "Usuario o contraseña incorrectos","is_logged_in": False}
        response = JsonResponse(data)
    return response


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def validarSesion(request):
    usuario = {
    'id': request.user.id,
    'username': request.user.username,
    'email': request.user.email
    }   
    if request.user:
        data = {'mensaje': 'Usuario Logueado','username':usuario,'is_logged_in':True}
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {'mensaje': 'No hay usuario logueado','is_logged_in':False}
        return Response(data)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
def finalizarSesion(request):
    logout(request)
    request.auth.delete()
    data = {'message': 'Usuario deslogueado', 'is_logged_in': False}
    response = JsonResponse(data)
    response.delete_cookie('session_id')
    return response