from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import *

def index(request):
    prod = Product.objects.all().values()
    context = {
        'products': prod
    }
    return render(request, 'shop/index.html', context)


def show(request, id):
    prod = Product.objects.get(id = id)
    context = {
        'myproduct': prod
    }
    return render(request, 'shop/decription_prod.html', context)


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        myuser = User.objects.get(id=request.user.id)
        myproduct =Product.objects.get(id=product_id)
        product_in_cart_obj = ProductInCart.objects.filter(Q(user_id=request.user.id) & Q(product_id=product_id)).values()
        if product_in_cart_obj:
            temp = product_in_cart_obj[0]['quantify'] + 1
            ProductInCart.objects.filter(Q(user_id=request.user.id) & Q(product_id=product_id)).update(quantify = temp)
        else:
            product_in_cart = ProductInCart(user_id=myuser, product_id=myproduct, quantify=1)
            product_in_cart.save()
        messages.success(request, (f"Товар: {myproduct.name} добавлен в корзину"))
        return redirect('home')
    else:
        return redirect('login')
    

def add_to_cart_plus(request, product_id):
    if request.user.is_authenticated:
        myuser = User.objects.get(id=request.user.id)
        myproduct =Product.objects.get(id=product_id)
        product_in_cart_obj = ProductInCart.objects.filter(Q(user_id=request.user.id) & Q(product_id=product_id)).values()
        if product_in_cart_obj:
            temp = product_in_cart_obj[0]['quantify'] + 1
            ProductInCart.objects.filter(Q(user_id=request.user.id) & Q(product_id=product_id)).update(quantify = temp)
        else:
            product_in_cart = ProductInCart(user_id=myuser, product_id=myproduct, quantify=1)
            product_in_cart.save()
        return redirect('show_cart')
    else:
        return redirect('login')
    

def remove_to_cart_minus(request, product_id):
    if request.user.is_authenticated:
        myuser = User.objects.get(id=request.user.id)
        myproduct =Product.objects.get(id=product_id)
        product_in_cart_obj = ProductInCart.objects.filter(Q(user_id=request.user.id) & Q(product_id=product_id)).values()
        if product_in_cart_obj:
            temp = product_in_cart_obj[0]['quantify'] - 1
            ProductInCart.objects.filter(Q(user_id=request.user.id) & Q(product_id=product_id)).update(quantify = temp)
        else:
            product_in_cart = ProductInCart(user_id=myuser, product_id=myproduct, quantify=1)
            product_in_cart.save()
        return redirect('show_cart')
    else:
        return redirect('login')
    

def show_cart(request):
    total = 0
    if request.user.is_authenticated:
        myuser = User.objects.get(id=request.user.id)
        product_in_cart_obj = ProductInCart.objects.filter(user_id=request.user.id).values('id','product_id','product_id__name', 'product_id__price', 'quantify')
        for prod in product_in_cart_obj:
            prod['calculated_value'] = prod['quantify'] * prod['product_id__price']
            total += (prod['quantify'] * prod['product_id__price'])
        context = {
            'products': product_in_cart_obj,
            'total': total
        }
        return render(request, 'shop/cart.html', context)
    else:
        return redirect('login')


def remove_from_cart(request, product_in_cart_id):
    print(product_in_cart_id)
    product_in_cart = ProductInCart.objects.get(id=product_in_cart_id)
    product_in_cart.delete()
    return redirect('show_cart')
