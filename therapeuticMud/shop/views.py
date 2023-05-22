from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *


def index(request):
    prod = Product.objects.all().values()
    context = {
        'products': prod
    }
    return render(request, 'shop/index.html', context)


def show(request, id):
    prod = Product.objects.get(id=id)
    reviews = Review.objects.filter(product_id=id).values('user_id__username','review_date', 'comment')
    if request.method == "POST":
        form = Review_form(request.POST)
        if form.is_valid():
            mycomment = form.cleaned_data['comment']
            myuser = User.objects.get(id=request.user.id)
            myreview = Review(product_id=prod, user_id=myuser, comment=mycomment)
            myreview.save()
    else:
        form = Review_form()
    context = {
        'myproduct': prod,
        'reviews': reviews,
        'form': form
    }
    return render(request, 'shop/decription_prod.html', context)


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        myuser = User.objects.get(id=request.user.id)
        myproduct = Product.objects.get(id=product_id)
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
        myproduct = Product.objects.get(id=product_id)
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
        myproduct = Product.objects.get(id=product_id)
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


def create_order(request):
    if request.user.is_authenticated:
        my_user = User.objects.get(id=request.user.id)
        order = Order(user_id=my_user)
        order.save()

        product_in_cart_obj = ProductInCart.objects.filter(user_id=request.user.id).values()
        for prod in product_in_cart_obj:
            my_product = Product.objects.get(id=prod['product_id_id'])
            order_details = OrderDetails(order_id=order, product_id=my_product, selling_price=my_product.price, quantify=prod['quantify'])
            order_details.save()

        messages.success(request, (f"Заказ номер: {order.id} создан"))
        return redirect('home')
    else:
        return redirect('login')


def show_orders(request):
    total = 0
    if request.user.is_staff:
        orders = Order.objects.values('user_id__username','order_date','id')
        for order in orders:
            order_details = OrderDetails.objects.filter(order_id=order['id']).values('product_id__name', 'selling_price', 'quantify')
            order['order_detail'] = order_details
            for order_detail in order_details:
                total += (order_detail['selling_price'] * order_detail['quantify'])
            order['total'] = total
            total = 0
        context = {
            'orders': orders,
        }
        print(orders)
        return render(request, 'shop/orders.html', context)
    else:
        return redirect('login')


def add_review(request):
    pass