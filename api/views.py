import uuid
from rest_framework import (
    permissions,
    status,
    views,
    exceptions,
    parsers
)
from rest_framework.response import Response
from rest_framework_csv import renderers as r
from api import models, serializers
from api.parsers import CSVParser


class RegistrationView(views.APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = serializers.ClientRegistrationSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientsView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        key = kwargs.get('id', None)
        if key:
            queryset = models.Client.objects.raw(
                "SELECT * FROM api_client WHERE id = %s LIMIT 1",
                (uuid.UUID(key).hex,)
            )

            if len(queryset) > 0:
                return Response(serializers.ClientSerializer(
                    queryset,
                    context={'request': request},
                    many=True
                ).data, status=status.HTTP_200_OK)
            raise exceptions.NotFound(
                detail="The requested client was not found."
            )

        queryset = models.Client.objects.raw("SELECT * FROM api_client")

        return Response(serializers.ClientSerializer(
            queryset,
            context={'request': request},
            many=True
        ).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request, *args, **kwargs):
        key = kwargs.get('id', None)
        if not key:
            return

        instance = None
        result = models.Client.objects.raw(
            "SELECT * FROM api_client WHERE id = %s LIMIT 1",
            (uuid.UUID(key).hex,)
        )

        if len(result) > 0:
            instance = result[0]
        else:
            raise exceptions.NotFound(
                detail="The requested client was not found."
            )

        serializer = serializers.ClientSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        key = kwargs.get('id', None)
        if not key:
            return

        instance = None
        result = models.Client.objects.raw(
            "SELECT * FROM api_client WHERE id = %s LIMIT 1",
            (uuid.UUID(key).hex,)
        )

        if len(result) > 0:
            instance = result[0]
        else:
            raise exceptions.NotFound(
                detail="The requested client was not found."
            )

        serializer = serializers.ClientSerializer(
            instance,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        key = kwargs.get('id', None)
        if not key:
            return

        instance = None
        result = models.Client.objects.raw(
            "SELECT * FROM api_client WHERE id = %s LIMIT 1",
            (uuid.UUID(key).hex,)
        )

        if len(result) > 0:
            instance = result[0]
        else:
            raise exceptions.NotFound(
                detail="The requested client was not found."
            )

        instance.delete()
        return Response(
            {
                'message': "The customer has been succesfully deleted"
            },
            status=status.HTTP_202_ACCEPTED
        )


class ClientsCSVView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    renderer_classes = (r.CSVRenderer, )

    def get(self, request):
        queryset = models.Client.objects.raw("SELECT * FROM api_client")

        return Response(serializers.ClientCSVSerializer(
            queryset,
            context={'request': request},
            many=True
        ).data, status=status.HTTP_200_OK)



class ClientsCSVImportView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    parser_classes = (parsers.MultiPartParser, )

    def put(self, request):
        file = request.FILES['data']
        parser = CSVParser(file, ',')
        data = parser.parse()

        serializer = serializers.ClientSerializer(
            data=data,
            many=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )



class ProductsView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        key = kwargs.get('id', None)
        if key:
            try:
                instance = models.Product.objects.get(pk=key)
                return Response(serializers.ProductSerializer(
                    instance,
                    context={'request': request}
                ).data, status=status.HTTP_200_OK)
            except models.Product.DoesNotExist as exc:
                raise exceptions.NotFound(
                    detail="The requested product was not found."
                ) from exc

        queryset = models.Product.objects.all()

        return Response(serializers.ProductSerializer(
            queryset,
            context={'request': request},
            many=True
        ).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request, *args, **kwargs):
        key = kwargs.get('id', None)
        if not key:
            return

        try:
            instance = models.Product.objects.get(pk=key)
        except models.Product.DoesNotExist as exc:
            raise exceptions.NotFound(
                detail="The requested product was not found."
            ) from exc

        serializer = serializers.ProductSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        key = kwargs.get('id', None)
        if not key:
            return

        try:
            instance = models.Product.objects.get(pk=key)
        except models.Product.DoesNotExist:
            raise exceptions.NotFound(detail="The requested product was not found.")

        serializer = serializers.ProductSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        key = kwargs.get('id', None)
        if not key:
            return

        try:
            instance = models.Product.objects.get(pk=key)
        except models.Product.DoesNotExist as exc:
            raise exceptions.NotFound(
                detail="The requested product was not found."
            ) from exc

        instance.delete()
        return Response(
            {
                'message': "The product has been succesfully deleted"
            },
            status=status.HTTP_202_ACCEPTED
        )


class BillsView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        key = kwargs.get('id', None)
        if key:
            queryset = models.Bill.objects.raw(
                "SELECT * FROM api_bill WHERE id = %s LIMIT 1",
                (key, )
            )

            if len(queryset) > 0:
                return Response(serializers.BillSerializer(
                    queryset,
                    context={'request': request},
                    many=True
                ).data, status=status.HTTP_200_OK)
            else:
                raise exceptions.NotFound(
                    detail="The requested bill was not found."
                )

        queryset = models.Bill.objects.raw("SELECT * FROM api_bill")

        return Response(serializers.BillSerializer(
            queryset,
            context={'request': request},
            many=True
        ).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.BillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request, *args, **kwargs):
        key = kwargs.get('id', None)
        if not key:
            return

        instance = None
        result = models.Bill.objects.raw(
            "SELECT * FROM api_bill WHERE id = %s LIMIT 1",
            (key, )
        )

        if len(result) > 0:
            instance = result[0]
        else:
            raise exceptions.NotFound(
                detail="The requested bill was not found."
            )

        serializer = serializers.BillSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        key = kwargs.get('id', None)
        if not key:
            return

        instance = None
        result = models.Bill.objects.raw(
            "SELECT * FROM api_bill WHERE id = %s LIMIT 1",
            (key, )
        )

        if len(result) > 0:
            instance = result[0]
        else:
            raise exceptions.NotFound(
                detail="The requested bill was not found."
            )

        serializer = serializers.BillSerializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        key = kwargs.get('id', None)
        if not key:
            return

        instance = None
        result = models.Bill.objects.raw(
            "SELECT * FROM api_bill WHERE id = %s LIMIT 1",
            (key, )
        )

        if len(result) > 0:
            instance = result[0]
        else:
            raise exceptions.NotFound(
                detail="The requested bill was not found."
            )

        instance.delete()
        return Response(
            {
                'message': "The bill has been succesfully deleted"
            },
            status=status.HTTP_202_ACCEPTED
        )
