from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager["User"]):
    class UserManager(BaseUserManager["User"]):
        def create_user(
                self, email, password=None, is_staff=False, is_active=True, **extra_fields
        ):
            """Create a user instance with the given email and password."""
            email = UserManager.normalize_email(email)
            # Google OAuth2 backend send unnecessary username field
            extra_fields.pop("username", None)

            user = self.model(
                email=email, is_active=is_active, is_staff=is_staff, **extra_fields
            )
            if password:
                user.set_password(password)
            user.save()
            return user


class Role(models.Model):
    """
        The Role entries are managed by the system,
        automatically created via a Django data migration.
    """
    CLIENT = 1
    MANAGER = 2
    OWNER = 3
    QC = 4
    ADMIN = 5
    ROLE_CHOICES = (
        (CLIENT, 'client'),
        (MANAGER, 'manager'),
        (OWNER, 'owner'),
        (QC, 'qc'),
        (ADMIN, 'admin'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    roles = models.ManyToManyField(Role)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = "date_joined"
        verbose_name = 'user'
        verbose_name_plural = 'users'
