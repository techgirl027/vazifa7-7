from django.shortcuts import render, redirect
from django.conf import settings
from . import models
from django.contrib.auth import authenticate, login, logout

# Create your views here.


# def home_page(request):
#     return render(request, "index.html")


def home_page(request):
    banners = models.Banner.objects.filter(is_active=True)[:5]
    navbars = models.Navbar.objects.all()
    context = {}
    context["banners"] = banners
    context["navbars"] = navbars

    return render(request, "index.html", context)


def register_page(request):
    email = request.POST["email"]
    password = request.POST["password"]
    models.Contact.objects.create(email=email, password=password)
    return render(request, "login-register.html")


def login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    if username:
        return redirect(request, home_page)
    return redirect(request, register_page)


def product_create(request):
    return render()
