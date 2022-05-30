from rest_framework import serializers
from .models import PaymentInfoModel


class PaymentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInfoModel
        fields = ['date', 'type', 'payment_mean', 'description', 'currency', 'amount', 'amount_in_pln']

