from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
import os
from django.conf import settings
from django.db.models.signals import post_save
# from .choices import departamento


#El siguiente bloque de código guarda la imagen de perfil del usuario
def user_directory_path_profile(instance,filename):
    profile_picture_name = 'user/{0}/profile.jpg'.format(instance.user.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name

class USer(AbstractBaseUser):
    stripe_custome_id = models.CharField(max_length=50)

class PerfilUsuario(models.Model):
    nombre1 = models.CharField(max_length=30, default="user")
    nombre2 = models.CharField(max_length=30, default="default")
    primerApellido = models.CharField(max_length=50,default="")
    segundoApellido = models.CharField(max_length=50,default="")
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    #departamento = models.CharField(max_length=50,choices = departamento, default = '')
    ciudad = models.CharField(max_length=50, default="")
    celular = models.CharField(max_length=10,default="")
    direccion = models.CharField(max_length=50,default="")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) :
        return self.nombre1

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create (user = instance)

def save_user_profile(sender,instance, **kwargs):
    instance.perfilusuario.save()

post_save.connect(create_user_profile, sender = User)
post_save.connect(save_user_profile, sender = User)