from django.shortcuts import render

def index(requset):
    return render(requset, 'shop/index.html')