from rest_framework import serializers
from . models import *
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorModel
        fields = ['name','contact','address']

class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorModel
        fields = ['on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderModel
        fields = ['items','vendor']

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformanceModel
        fields = '__all__'




