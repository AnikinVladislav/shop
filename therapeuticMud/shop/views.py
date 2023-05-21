from django.shortcuts import render, redirect
from .models import *

def index(requset):
    prod = Product.objects.all().values()
    context = {
        'products': prod
    }
    return render(requset, 'shop/index.html', context)


def show(requset, id):
    print(id)
    prod = Product.objects.get(id = id)
    print(prod)
    context = {
        'myproduct': prod
    }
    return render(requset, 'shop/decription_prod.html', context)


def add_to_cart(request, product_id, quantify):
    if request.user.is_authenticated:
        product_in_cart = ProductInCart(user_id=request.user.id, product_id=product_id, quantify=quantify)
        product_in_cart.save()

        # Redirect to a success page or display a message
        return redirect('success_page')
    else:
        return redirect('login_page')


def remove_from_cart(request, product_in_cart_id):
    product_in_cart = ProductInCart.objects.get(id=product_in_cart_id)
    product_in_cart.delete()

    #show_cart()
    # return render(request, 'cart.html', )
