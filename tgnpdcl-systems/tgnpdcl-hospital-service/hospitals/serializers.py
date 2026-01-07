from rest_framework import serializers
from .models import Hospital, Bill, LineItem, Service

class LineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItem
        fields = '__all__'
        read_only_fields = ('amount',)

class BillSerializer(serializers.ModelSerializer):
    items = LineItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Bill
        fields = '__all__'
        read_only_fields = ('status', 'submission_date', 'tgnpdcl_id')

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'
