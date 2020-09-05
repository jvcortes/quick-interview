import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class ClientManager(BaseUserManager):
    def get_by_natural_key(self, email_):
        return self.get(email=email_)


class Client(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    objects = ClientManager()

    USERNAME_FIELD = 'email'


class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE
    )
    company_name = models.CharField(max_length=255)
    nit = models.CharField(max_length=255)
    products = models.ManyToManyField(
        'Product',
    )
    code = models.IntegerField()


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
