from django.urls import path, include

urlpatterns = [
    path("product/", include("app.back-office.product.urls")),
    path("category/", include("app.back-office.category.urls")),
]
