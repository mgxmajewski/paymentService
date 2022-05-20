from django.db import models


# Create your models here.
class PayByLink(models.Model):
    created_at = models.CharField(max_length=1)

