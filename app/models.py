from django.db import models
from django.contrib.auth.models import User
from random import sample
import string


class GenereteCode(models.Model):
    generete_code = models.CharField(max_length=255, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.generete_code:
            self.generete_code = "".join(sample(string.ascii_letters, 20))
        super(GenereteCode, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Banner(GenereteCode):
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    img = models.ImageField(upload_to="banners/")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Category(GenereteCode):
    name = models.CharField(max_length=255)
    img = models.ImageField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(GenereteCode):
    name: str = models.CharField(max_length=255)
    quantity: int = models.PositiveIntegerField(default=1)
    price: float = models.DecimalField(max_digits=8, decimal_places=2)
    category: Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description: str = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductEnter(GenereteCode):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantitiy = models.IntegerField()
    old_quantity = models.IntegerField(blank=True)
    date = models.DateTimeField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.product.name

    def save(self, *args, **kwargs):
        if not self.generete_code:
            self.old_quantity = self.product.quantity
            self.product.quantity = self.quantitiy
        else:
            self.product.quantity -= ProductEnter.objects.get(
                generete_code=self.generete_code
            ).quantitiy
            self.product.quantity += self.quantitiy
        self.product.save()
        super(ProductEnter, self).save(*args, **kwargs)


class ProductImg(GenereteCode):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="product-img")

    def __str__(self):
        return self.product.name


class Cart(GenereteCode):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    shopping_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.author.username


class CartProduct(GenereteCode):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name


class Order(GenereteCode):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=255)
    status = models.SmallIntegerField(
        choices=(
            (1, "Tayyorlanmoqda"),
            (2, "Yo`lda"),
            (3, "Yetib borgan"),
            (4, "Qabul qilingan"),
            (5, "Qaytarilgan"),
        )
    )

    def __str__(self):
        return self.full_name


class Navbar(GenereteCode):
    title = models.CharField(max_length=255)
    email = models.EmailField()
    tel = models.IntegerField()
    location = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}, {self.product.name}"
