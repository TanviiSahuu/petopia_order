from rest_framework import serializers
from .models import Order, OrderDetails, Payment

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['order_id', 'order_date_time']  # Auto-generated fields

class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'  
        read_only_fields = ['order_details_id'] 

class PaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(source="order.order_id", write_only=True)  # Accept order_id instead of order

    class Meta:
        model = Payment
        fields = ["order_id", "amount", "method", "status"]

    def create(self, validated_data):
        order_id = validated_data.pop("order")["order_id"]  # Extract order ID
        order = Order.objects.get(order_id=order_id)  # Fetch Order instance
        return Payment.objects.create(order=order, **validated_data)
