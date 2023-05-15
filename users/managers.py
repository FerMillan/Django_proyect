from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class AccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        extra_fields.setdefault('tipo', 2)
        
        if not email:
            raise ValueError(_('Debes tener un email'))
        if not username:
            raise ValueError(_('Debes tener un usuario'))
        email = self.normalize_email(email)
        user = self.model(correo=email, **extra_fields)
        user = self.model(usuario=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, usuario, correo, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('tipo', 1)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser debe tener is_superuser=True.'))
        extra_fields.setdefault('tipo', 3)
        
        if not correo:
            raise ValueError(_('Debes tener un correo'))
        if not usuario:
            raise ValueError(_('Debes tener un usuario'))
        correo_ = self.normalize_email(correo)
        user = self.model(correo=correo_, **extra_fields)
        user = self.model(usuario=usuario, **extra_fields)
        user.set_password(password)
        user.save()
        return user