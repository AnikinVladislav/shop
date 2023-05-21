from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:id>', views.show, name='show'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('show_cart', views.show_cart, name='show_cart'),
    path('remove_from_cart/<int:product_in_cart_id>', views.remove_from_cart, name='remove_from_cart'),
    path('add_to_cart_plus/<int:product_id>', views.add_to_cart_plus, name='add_to_cart_plus'),
    path('remove_to_cart_minus/<int:product_id>', views.remove_to_cart_minus, name='remove_to_cart_minus'),
]