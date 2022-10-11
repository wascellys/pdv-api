from decimal import Decimal
import datetime
import django
from django.db import models


class Product(models.Model):
    TYPE_PRODUCT = (
        ("product", "Product"),
        ("service", "Service"),
    )
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.CharField(max_length=100, blank=False, null=False)
    type = models.CharField(max_length=100, choices=TYPE_PRODUCT, blank=False, null=False)
    commission = models.CharField(max_length=10, blank=False, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)



class Person(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Seller(Person):

    def __str__(self):
        return self.name


class Client(Person):

    def __str__(self):
        return self.name


class Sale(models.Model):
    date = models.DateTimeField(default=django.utils.timezone.now)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sale_commission = models.CharField(max_length=20, null=True, blank=True)
    total = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.seller.name)


    def calc_commission(self, commissions, date_max_final, date_max_init, product, time_sale):
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

        self.sale_commission = round(sum(commissions), 2)


class OrdersSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)
