"""
Contains the models for the `api` application.
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class ClientManager(BaseUserManager):
    """
    ClientManager - User manager for the Client class
    """
    def get_by_natural_key(self, email_):
        """
        Allows authentication services to use the `email` field as
        an identifier for the `Client` class instance.
        """
        return self.get(email=email_)


class Client(AbstractBaseUser):
    """
    Client - Defines a client and its authentication details

    The `email` field will be used as its username field.

    Class attributes:
        id: UUID identifier
        document: Clients's identity document
        first_name: Clients's first name
        last_name: Clients's last name
        emal: Clients's email
        objects = Client class user manager
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    objects = ClientManager()

    USERNAME_FIELD = 'email'


class Bill(models.Model):
    """
    Bill - Defines a bill

    Class attributes:
        id: Autoincremental integer identifier
        client: Bill client
        company_name: Name for the company in which the bill was made for
        nit: NIT for the company in which the bill was made for
        products: List of purchased products
    """
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
    """
    Product - Defines a product

    Class attributes:
        id: UUID identifier
        name: Product name
        name: Product description
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
