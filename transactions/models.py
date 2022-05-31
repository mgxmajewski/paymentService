from django.db import models


class ReportModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField()


class PaymentInfoModel(models.Model):
    report = models.ForeignKey('ReportModel', on_delete=models.CASCADE)
    date = models.CharField(max_length=40)
    type = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    currency = models.CharField(max_length=30)
    payment_mean = models.CharField(max_length=30)
    amount = models.IntegerField()
    amount_in_pln = models.IntegerField()
