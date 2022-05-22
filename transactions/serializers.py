from abc import ABC

from rest_framework import serializers
# from .models import PayByLink

#
# class PayByLinkSerializer(serializers.Serializer):
#     date = serializers.CharField(max_length=30, source='crated_at')
#     currency = serializers.CharField(max_length=3)
#     amount = serializers.IntegerField()
#     description = serializers.CharField(max_length=20)
#     bank = serializers.CharField(max_length=10)
