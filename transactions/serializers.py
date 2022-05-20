from rest_framework import serializers
from .models import PayByLink


class PayByLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayByLink
        fields = '__all__'
