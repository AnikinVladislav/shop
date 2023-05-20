from django.db import models

class Product(models.Model):
    """
    price - decimal_places=2 - количество знаков после запятой
    """
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    quantify = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name}'