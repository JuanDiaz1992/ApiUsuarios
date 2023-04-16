from django.urls import path
from .views import iniciarSesion, validarSesion,finalizarSesion


urlpatterns = [
    path('iniciar/', iniciarSesion, name='User'),
    path('validarSesion/', validarSesion, name='validarSesion' ),
    path('finalizarSesion/', finalizarSesion, name='finalizarSesion' )

]
