from django.db import models


class PaymentInfoModel(models.Model):
    date = models.CharField(max_length=40)
    type = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    currency = models.CharField(max_length=30)
    payment_mean = models.CharField(max_length=30)
    amount = models.IntegerField()
    amount_in_pln = models.IntegerField()
