from django.conf import settings
from django.db import models
from django.utils import timezone


# Create your models here.

class Product(models.Model):
    class Status(models.IntegerChoices):
        SOLD = 1
        UNSOLD = 2

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
    status = models.IntegerField(choices=Status.choices, null=False)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class PurchaseHistory(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.ForeignKey('handshake_market.Product', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=19, decimal_places=2)


class SellingHistory(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.ForeignKey('handshake_market.Product', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=19, decimal_places=2)


class CashIn(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
