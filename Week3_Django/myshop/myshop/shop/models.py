from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=150, null=False)
    address = models.JSONField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ProductCategory(models.Model):
    name = models.CharField(max_length=150, null=False)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    name = models.CharField(max_length=150, null=False)
    description = models.TextField(null=True)
    remaining_amount = models.IntegerField(null=False, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    categories = models.ManyToManyField("shop.ProductCategory")

    def __str__(self):
        return f"{self.name}"

class Cart(models.Model):
    customer = models.IntegerField(null=False)
    customer = models.ForeignKey("shop.Customer", on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    expired_in = models.IntegerField(null=False, default=60)

    def __str__(self):
        return f"{self.customer}"

class CartItem(models.Model):
    cart = models.IntegerField(null=False)
    cart = models.ForeignKey("shop.Cart", on_delete=models.CASCADE)
    product = models.IntegerField(null=False)
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE)
    amount = models.IntegerField(null=False, default=1)

    def __str__(self):
        return f"{self.product}"

class Order(models.Model):
    customer = models.IntegerField(null=False)
    customer = models.ForeignKey("shop.Customer", on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True, null=False)
    remark = models.TextField(null=True)

    def __str__(self):
        return f"{self.customer}"

class OrderItem(models.Model):
    order = models.IntegerField(null=False)
    order = models.ForeignKey("shop.Order", on_delete=models.CASCADE)
    product = models.IntegerField(null=False)
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE)
    amount = models.IntegerField(null=False, default=1)

    def __str__(self):
        return f"{self.product}"

class Payment(models.Model):
    order = models.IntegerField(null=False)
    order = models.OneToOneField("shop.Order", on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True, null=False)
    remark = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def __str__(self):
        return f"{self.order}"

class PaymentItem(models.Model):
    payment = models.IntegerField(null=False)
    payment = models.ForeignKey("shop.Payment", on_delete=models.CASCADE)
    order_item = models.IntegerField(null=False)
    order_item = models.OneToOneField("shop.OrderItem", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def __str__(self):
        return f"{self.order_item}"

class PaymentMethod(models.Model):
    class MethodChoice(models.TextChoices):
        QR = "QR", "QR"
        CREDIT = "CREDIT", "Credit Cart"

    payment = models.IntegerField(null=False)
    payment = models.ForeignKey("shop.Payment", on_delete=models.CASCADE)
    method = models.CharField(choices=MethodChoice, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return f"{self.method}"