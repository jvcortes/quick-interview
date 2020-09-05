from rest_framework import serializers, validators
from api import models


class ClientRegistrationSerializer(serializers.ModelSerializer):
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
        model = models.Client
        fields = ('email', 'password', 'document')

    def save(self):
        password = self.validated_data.pop('password')
        client = models.Client(**self.validated_data)
        client.set_password(password)
        client.save()


class ClientSerializer(serializers.ModelSerializer):
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

    bill_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
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
        return obj.bill_set.count()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = (
            'id',
            'name',
            'description'
        )

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bill
        fields = (
            'id',
            'client',
            'company_name',
            'nit',
            'products',
            'code'
        )
