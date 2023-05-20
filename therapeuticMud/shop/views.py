from django.shortcuts import render
from .models import *

def index(requset):
    prod = Product.objects.all().values()
    print(prod)
    context = {
        'products': prod
    }
    return render(requset, 'shop/index.html', context)