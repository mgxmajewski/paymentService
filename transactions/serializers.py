from rest_framework import serializers
from .models import PaymentInfoModel, ReportModel


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportModel
        fields = ['user']


class PaymentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInfoModel
        fields = ['report', 'date', 'type', 'payment_mean', 'description', 'currency', 'amount', 'amount_in_pln']
