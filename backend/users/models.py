from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.core.exceptions import ValidationError

USER_TYPES = [
    ('buyer', 'Buyer'),
    ('seller', 'Seller'),
    ('admin', 'Admin'),
]

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPES,
        default='buyer',
    )
    company_name = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def clean(self):
        if self.user_type == 'seller' and not self.company_name:
            raise ValidationError("Sellers must provide a company name.")
        if self.user_type == 'buyer' and self.company_name:
            raise ValidationError("Buyers should not provide a company name.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        if self.user_type == 'admin' and self.is_superuser:
            admin_group, _ = Group.objects.get_or_create(name='Admin')
            self.groups.add(admin_group)

    def __str__(self):
        return self.email
