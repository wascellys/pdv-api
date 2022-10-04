from django.contrib import admin

from api.models import Client, Product, Seller, Sale, OrdersSale

# Register your models here.

admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Seller)
admin.site.register(Sale)
admin.site.register(OrdersSale)
