from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    quantify = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name}'


class ProductInCart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantify = models.PositiveIntegerField()


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField(null=False) 
    payment_method = models.CharField(max_length = 1, choices=[( 0, "Наличный расчет"), ( 1, "Безналичный расчет")], default = 1)


class OrderDetails(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantify = models.PositiveIntegerField()


class Review(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=False)
    review_date = models.DateTimeField(auto_now_add=True)
