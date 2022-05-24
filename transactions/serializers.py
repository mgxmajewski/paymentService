from rest_framework import serializers
from .models import PaymentInfoModel


class PaymentInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInfoModel
        fields = ['date', 'type', 'payment_mean', 'description', 'currency', 'amount', 'amount_in_pln']


class PaymentInfoSerializer(serializers.Serializer):
    id: serializers.IntegerField(read_only=True)
    date: serializers.CharField(max_length=30)
    type: serializers.CharField(max_length=30)
    amount: serializers.IntegerField()
    description: serializers.CharField(max_length=30)
    currency: serializers.CharField(max_length=30)
    payment_mean: serializers.CharField(max_length=30)
    amount_in_pln: serializers.IntegerField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return PaymentInfoModel.objects.create(**validated_data)
