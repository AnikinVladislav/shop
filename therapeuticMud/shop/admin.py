from django.contrib import admin
from .models import Product, ProductInCart, Order, OrderDetails


# Register your models here.
admin.site.register(Product)
admin.site.register(ProductInCart)
admin.site.register(Order)
admin.site.register(OrderDetails)
