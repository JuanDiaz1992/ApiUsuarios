from django.urls import path
from .views import userView

urlpatterns = [
    path('usuarios/', userView.as_view(), name='User'),

]
