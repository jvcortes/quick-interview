"""
Contains the serializers.
"""
from rest_framework import serializers, validators
from api import models


class ClientRegistrationSerializer(serializers.ModelSerializer):
    """
    ClientRegistrationSerializer - Serializes the data required for a client's
    registration process.

    Class attributes:
        email: email field, is required and must be unique
        email: password field, is required
        document: document field, is required and must be unique
    """
    email = serializers.EmailField(
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=models.Client.objects.extra(
                    select={'val': "SELECT * FROM api_client"}
                )
            )
        ]
    )
    password = serializers.CharField(required=True, write_only=True)
    document = serializers.CharField(
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=models.Client.objects.extra(
                    select={'val': "SELECT * FROM api_client"}
                )
            )
        ]
    )

    class Meta:
        """
        Meta - Metadata for the `ClientRegistrationSerializer` class.
        """
        model = models.Client
        fields = ('email', 'password', 'document')

    def save(self):
        """
        save - Saves a new `Client` instance.
        """
        password = self.validated_data.pop('password')
        client = models.Client(**self.validated_data)
        client.set_password(password)
        client.save()


class ClientSerializer(serializers.ModelSerializer):
    """
    ClientSerializer - Serializes `Client` instances.
    """
    class Meta:
        model = models.Client
        fields = (
            'id',
            'document',
            'email',
            'first_name',
            'last_name',
            'last_login'
        )

class ClientCSVSerializer(serializers.ModelSerializer):
    """
    ClientSerializer - Serializes `Client` instances, used for the CSV
    export endpoint.

    Class attributes:
        bill_count: total count of the bills that a client has
    """
    bill_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """
        Meta - Metadata for the `ClientCSVSerializer` class.
        """
        model = models.Client
        fields = (
            'id',
            'document',
            'email',
            'first_name',
            'last_name',
            'bill_count'
        )

    def get_bill_count(self, obj):
        """
        get_bill_count - gets the total bill count for a `Client` instance.

        Parameters:
            obj: `Client` instance
        """
        return obj.bill_set.count()


class ProductSerializer(serializers.ModelSerializer):
    """
    ProductSerializer - Serializes `Product` instances.
    """
    class Meta:
        """
        Meta - Metadata for the `ProductSerializer` class.
        """
        model = models.Product
        fields = (
            'id',
            'name',
            'description'
        )


class BillSerializer(serializers.ModelSerializer):
    """
    BillSerializer - Serializes `Bill` instances.
    """
    class Meta:
        """
        Meta - Metadata for the `BillSerializer` class.
        """
        model = models.Bill
        fields = (
            'id',
            'client',
            'company_name',
            'nit',
            'products',
            'code'
        )
