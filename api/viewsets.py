import datetime
from decimal import Decimal

from decouple import config
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from api.models import Client, Seller, Product, Sale, OrdersSale
from api.serializers import ClientSerializer, SellerSerializer, ProductSerializer, SaleSerializer, OrdersSaleSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_queryset(self):
        return self.queryset


class SellerViewSet(ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

    def get_queryset(self):
        return self.queryset

    @action(detail=True, methods=['get'])
    def commission(self, request, pk=None):
        try:
            sales = Sale.objects.filter(seller__pk=pk)
            params = request.query_params
            if params:
                initial_date = datetime.datetime.strptime(params.get("initial_date"), '%d/%m/%Y')
                final_date = datetime.datetime.strptime(params.get("final_date"), '%d/%m/%Y')
                sales = sales.filter(date__gte=initial_date, date__lte=final_date)
            total = [Decimal(i.sale_commission) for i in sales]
            total = round(sum(total), 2)
            serializer = SaleSerializer(sales, many=True)
            return Response(data={"data": serializer.data, "total": total}, status=status.HTTP_200_OK)
        except (Exception,):
            return Response(data={"message": "invalid params"}, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.queryset


class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def list(self, request):
        serializers = self.serializer_class(self.queryset, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            with transaction.atomic():
                sale = Sale()
                sale.seller = Seller.objects.get(id=data.get("seller"))
                sale.client = Client.objects.get(id=data.get("client"))
                sale.save()

                serializers = self.serializer_class(sale)
                commissions = []
                total = []
                for order in data.get("orders"):
                    for i in range(order[1]):
                        product = Product.objects.get(id=order[0])
                        total.append(Decimal(product.price))
                        OrdersSale.objects.create(product=product, sale=sale)
                        time_sale = sale.date.time()
                        date_max_init = config("DATE_INIT_MAX").split(",")
                        date_max_final = config("DATE_FINAL_MAX").split(",")
                        if time_sale > datetime.time(int(date_max_init[0]), int(date_max_init[1]),
                                                     int(date_max_init[2])) and time_sale < datetime.time(
                            int(date_max_final[0]),
                            int(date_max_final[1]),
                            int(date_max_final[2])):
                            commissions.append(Decimal(product.commission) / 100 * Decimal(product.price) if Decimal(
                                product.commission) <= 5 else Decimal(5 / 100) * Decimal(product.price))
                        else:
                            commissions.append(Decimal(4 / 100) * Decimal(product.price) if Decimal(
                                product.commission) <= 4 else Decimal(product.commission) / 100 * Decimal(
                                product.price))

                sale.sale_commission = round(sum(commissions), 2)
                sale.total = round(sum(total), 2)

                sale.save()
                return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        except (Exception,):
            return Response({'message': 'Error processing the sale'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            sale = Sale.objects.get(id=kwargs['pk'])
            serializers = self.serializer_class(sale)
            return Response(data=serializers.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Data does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            sale = Sale.objects.get(id=kwargs['pk'])
            serializer = self.serializer_class(sale, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'message': 'Data does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        orders = OrdersSale.objects.filter(sale__pk=pk)
        serializer = OrdersSaleSerializer(orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class OrdersSaleViewSet(ModelViewSet):
    queryset = OrdersSale.objects.all()
    serializer_class = OrdersSaleSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'message': 'Error to insert'}, status=status.HTTP_400_BAD_REQUEST)
        except (Exception,):
            return Response({'message': 'Error to insert'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            order = OrdersSale.objects.get(id=kwargs['pk'])
            serializers = self.serializer_class(order)
            return Response(data=serializers.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Data does not exist!'}, status=status.HTTP_404_NOT_FOUND)
        except (Exception,):
            return Response({'message': ''}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            order = OrdersSale.objects.get(id=kwargs['pk'])
            serializer = self.serializer_class(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'message': 'Data does not exist!'}, status=status.HTTP_404_NOT_FOUND)
