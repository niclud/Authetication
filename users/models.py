from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('El email debe ser obligatorio')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):

        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class Users(AbstractBaseUser, PermissionsMixin):
    # Campos de autenticación
    email = models.EmailField(unique=True)
    # username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # La contraseña se almacena con hash en la base de datos

    # Información personal
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(blank=True, null=True)
    # bio = models.TextField(blank=True)

    # Campos adicionales
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Campo que se usa para autenticar
    class Meta:
        # Especifica un related_name único para grupos y user_permissions
        permissions = (
            ("custom_can_do_something", "Can do something custom"),
        )

    # Especifica un related_name único para la relación con grupos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users_groups',
        related_query_name='custom_user_group',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    # Especifica un related_name único para la relación con permisos
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users_permissions',
        related_query_name='custom_user_permission',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )