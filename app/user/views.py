from django.shortcuts import render, redirect, get_object_or_404
from app import models


def myCart(request):
    cart = models.Cart.objects.filter(author=request.user, is_active=True)
    context = {}
    context["cart"] = cart
    return render(request, "cart.html", context)


def addProductToCart(request):
    code = request.GET["code"]
    quantity = request.GET["quantity"]
    product = models.Product.objects.get(generete_code=code)
    cart, _ = models.Cart.objects.get_or_create(author=request.user, is_active=True)
    try:
        cart_product = models.CartProduct.objects.get(cart=cart, product=product)
        cart_product.quantity += quantity
        cart_product.save()
    except:
        cart_product = models.CartProduct.objects.create(
            product=product, cart=cart, quantity=quantity
        )
    return redirect("/")


def substractProductFromCart(request):
    code = request.GET["code"]
    quantity = request.GET["quantity"]
    product_cart = models.CartProduct.objects.get(generete_code=code)
    product_cart.quantity -= quantity
    product_cart.save()
    if not product_cart.quantity:
        product_cart.delete()
    return redirect("/")


def deleteProductCart(request):
    code = request.GET["code"]
    product_cart = models.CartProduct.objects.get(generete_code=code)
    product_cart.delete()
    return redirect("/")


def CreateOrder(request):
    cart = models.Cart.objects.get(generete_code=request.GET["generete_code"])

    cart_products = models.CartProduct.objects.filter(cart=cart)

    done_products = []

    for cart_product in cart_products:
        if cart_product.quantity <= cart_product.product.quantity:
            cart_product.product.quantity -= cart_product.quantity
            cart_product.product.save()
            done_products.append(cart_product)
        else:
            for product in done_products:
                product.product.quantity += product.quantity
                product.product.save()
            raise ValueError("Qoldiqda kamchilik")

    models.Order.objects.create(
        cart=cart,
        full_name=f"{request.user.first_name}, {request.user.last_name}",
        email=request.user.email,
        phone=request.GET["phone"],
        address=request.GET["address"],
        status=1,
    )
    cart.is_active = False
    cart.save()

    return redirect("/")


def wishList(request):
    wish_list = models.WishList.objects.filter(user=request.user)
    data = []
    for wish in wish_list:
        a = models.ProductImg.objects.get(product=wish.product)
        data.append(a)
    context = {}
    combined = zip(wish_list, data)
    context["combined"] = combined

    return render(request, "wishlist.html", context)


def addOrDeleteWishList(request, id):
    product = get_object_or_404(models.Product, id=id)

    data, created = models.WishList.objects.get_or_create(
        product=product,
        user=request.user,
    )
    if not created:
        data.delete()

    next_url = request.META.get("HTTP_REFERER", "shop")
    return redirect(next_url)


def userSearch(request):
    q = request.GET.get("q")
    if q:
        result = models.Product.objects.filter(name=q)
        return render(request, "user/query.html", {"result": result})
    return redirect("/")
