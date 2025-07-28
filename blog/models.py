from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    narx = models.PositiveIntegerField()

    def __str__(self):
        return self.nom

class Order(models.Model):
    product = models.ManyToManyField(Product, through='OrderItem')
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    location = models.CharField(max_length=255, blank=True)
    sana = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # default muhim!


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.balance} so'm"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)






