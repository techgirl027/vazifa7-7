from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.myCart, name="cart"),
    path("wishlist", views.wishList, name="wishlist"),
]
