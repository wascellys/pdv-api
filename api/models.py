from datetime import datetime

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


class OrdersSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)
