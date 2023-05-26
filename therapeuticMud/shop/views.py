from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *
from .key import SECRET_KEY, SHOP_ID
import uuid
from yookassa import Configuration, Payment

Configuration.account_id = SHOP_ID
Configuration.secret_key = SECRET_KEY


def index(request):
    prod = Product.objects.all().values()

    order_id = request.session.pop('order_id', None)
    payment_id = request.session.pop('payment_id', None)
    if payment_id and order_id:
        payment = Payment.find_one(payment_id)
        if payment.status == 'succeeded':
            Order.objects.filter(id=order_id).update(payment_status="1")
            # remove products from cart
            ProductInCart.objects.filter(user_id=request.user.id).delete()
            messages.success(request, (f"Заказ номер: {order_id} создан"))
        else:
            Order.objects.filter(id=order_id).delete()

    context = {
        'products': prod
    }
    return render(request, 'shop/index.html', context)


def show(request, id):
    product = Product.objects.get(id=id)
    reviews = Review.objects.filter(product_id=id).values('user_id__username', 'review_date', 'comment').order_by('-review_date')
    if request.method == "POST":
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                my_comment = form.cleaned_data['comment']
                my_user = User.objects.get(id=request.user.id)
                my_review = Review(product_id=product, user_id=my_user, comment=my_comment)
                my_review.save()
        else:
            return redirect('login')
    else:
        form = ReviewForm()
    context = {
        'myproduct': product,
        'reviews': reviews,
        'form': form
    }
    return render(request, 'shop/decription_prod.html', context)


def show_cart(request):
    total = 0
    if request.user.is_authenticated:
        products_in_cart = ProductInCart.objects.filter(user_id=request.user.id).values('id', 'product_id',
                                                                                        'product_id__name',
                                                                                        'product_id__price', 'quantify')
        for product_in_cart in products_in_cart:
            product_in_cart['calculated_value'] = product_in_cart['quantify'] * product_in_cart['product_id__price']
            total += (product_in_cart['quantify'] * product_in_cart['product_id__price'])
        request.session['total'] = float(total)
        context = {
            'products': products_in_cart,
            'total': total
        }
        return render(request, 'shop/cart.html', context)
    else:
        return redirect('login')


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        my_user = User.objects.get(id=request.user.id)
        my_product = Product.objects.get(id=product_id)
        product_in_cart_obj = ProductInCart.objects.filter(
            Q(user_id=request.user.id) & Q(product_id=product_id)).values()
        if product_in_cart_obj:
            temp_quantify = product_in_cart_obj[0]['quantify'] + 1
            ProductInCart.objects.filter(Q(user_id=request.user.id) & Q(product_id=product_id)).update(
                quantify=temp_quantify)
        else:
            product_in_cart = ProductInCart(user_id=my_user, product_id=my_product, quantify=1)
            product_in_cart.save()
        messages.success(request, (f"Товар: {my_product.name} добавлен в корзину"))
        return redirect('home')
    else:
        return redirect('login')


def add_to_cart_plus(request, product_id):
    if request.user.is_authenticated:
        my_user = User.objects.get(id=request.user.id)
        my_product = Product.objects.get(id=product_id)
        product_in_cart_obj = ProductInCart.objects.filter(
            Q(user_id=request.user.id) & Q(product_id=product_id)).values()
        if product_in_cart_obj:
            temp_quantify = product_in_cart_obj[0]['quantify'] + 1
            ProductInCart.objects.filter(Q(user_id=request.user.id) & Q(product_id=product_id)).update(
                quantify=temp_quantify)
        else:
            product_in_cart = ProductInCart(user_id=my_user, product_id=my_product, quantify=1)
            product_in_cart.save()
        return redirect('show_cart')
    else:
        return redirect('login')


def remove_to_cart_minus(request, product_id):
    if request.user.is_authenticated:
        my_user = User.objects.get(id=request.user.id)
        my_product = Product.objects.get(id=product_id)
        products_in_cart = ProductInCart.objects.filter(Q(user_id=request.user.id) & Q(product_id=product_id)).values()
        if products_in_cart:
            temp_quantify = products_in_cart[0]['quantify'] - 1
            ProductInCart.objects.filter(Q(user_id=request.user.id) & Q(product_id=product_id)).update(
                quantify=temp_quantify)
        else:
            product_in_cart = ProductInCart(user_id=my_user, product_id=my_product, quantify=1)
            product_in_cart.save()
        return redirect('show_cart')
    else:
        return redirect('login')


def remove_from_cart(request, product_in_cart_id):
    # remove product from cart
    ProductInCart.objects.filter(id=product_in_cart_id).delete()
    return redirect('show_cart')


def confirm_order(request):
    if request.user.is_authenticated:
        products_in_cart = ProductInCart.objects.filter(user_id=request.user.id).values('product_id_id', 'quantify',
                                                                                        'product_id__quantify',
                                                                                        'product_id__name')
        if check_cart(request, products_in_cart):
            return redirect('show_cart')

        total = request.session.get('total', None)

        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                address = form.cleaned_data['address']
                payment_method = form.cleaned_data['payment_method']

                order_id = create_order(request, address, payment_method, products_in_cart)

                if payment_method == '1':
                    payment = create_payment(total, order_id)
                    request.session['order_id'] = order_id
                    request.session['payment_id'] = payment.id

                    # get confirmation url
                    confirmation_url = payment.confirmation.confirmation_url
                    return redirect(confirmation_url)
                elif payment_method == '0':
                    # remove products from cart
                    ProductInCart.objects.filter(user_id=request.user.id).delete()
                    messages.success(request, (f"Заказ номер: {order_id} создан"))
                    return redirect('home')
        else:
            form = OrderForm()
        context = {
            'total': total,
            'form': form
        }
        return render(request, 'shop/order_form.html', context)
    else:
        return redirect('home')


def check_cart(request, products_in_cart):
    # determine if there is something in the cart
    if not products_in_cart.exists():
        messages.success(request, (f"Корзина пуста, добавьте что-нибудь"))
        return True

    # determine whether there is a required quantity of goods
    for product_in_cart in products_in_cart:
        if product_in_cart['quantify'] > product_in_cart['product_id__quantify']:
            messages.success(request, (f"Заказ невозможен, уменьшите кол-во товара: {product_in_cart['product_id__name']}"))
            return True
    return False


def create_order(request, address, payment_method, products_in_cart):
    # write the order to the DB
    my_user = User.objects.get(id=request.user.id)
    order = Order(user_id=my_user, address=address, payment_method=payment_method)
    order.save()

    # write the details of the order to the DB
    for product_in_cart in products_in_cart:
        my_product = Product.objects.get(id=product_in_cart['product_id_id'])
        order_details = OrderDetails(order_id=order, product_id=my_product, selling_price=my_product.price,
                                     quantify=product_in_cart['quantify'])
        order_details.save()
    return order.id


def create_payment(total, order_id):
    payment = Payment.create({
        "amount": {
            "value": total,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://127.0.0.1:8000/"
        },
        "capture": True,
        "description": f"Заказ №{order_id}"
    }, uuid.uuid4())
    return payment


def show_orders(request):

    if request.user.is_authenticated:
        if request.user.is_staff:
            orders = Order.objects.values('user_id__username', 'order_date', 'id', 'address', 'payment_method',
                                      'payment_status').order_by('-order_date')
        else:
            orders = Order.objects.filter(user_id=request.user.id).values('user_id__username', 'order_date', 'id', 'address', 'payment_method',
                                          'payment_status').order_by('-order_date')
        total = 0
        # adding order details to orders
        for order in orders:
            order_details = OrderDetails.objects.filter(order_id=order['id']).values('product_id__name',
                                                                                     'selling_price', 'quantify')
            order['order_detail'] = order_details

            # calculate the cost of the order and add to the order
            for order_detail in order_details:
                total += (order_detail['selling_price'] * order_detail['quantify'])
            order['total'] = total
            total = 0

        context = {
            'orders': orders,
        }
        return render(request, 'shop/orders.html', context)
    else:
        return redirect('login')
