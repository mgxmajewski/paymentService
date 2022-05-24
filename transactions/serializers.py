from rest_framework import serializers


class PaymentInfoSerializer(serializers.Serializer):
    date: serializers.CharField(max_length=30)
    type: serializers.CharField(max_length=30)
    amount: serializers.IntegerField()
    description: serializers.CharField(max_length=30)
    currency: serializers.CharField(max_length=30)
    payment_mean: serializers.CharField(max_length=30)
    amount_in_pln: serializers.IntegerField()
