from rest_framework import serializers
from products.serializers import ProductListSerializer
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'price', 'total')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'order_number', 'user', 'status', 'payment_status', 
                  'payment_method', 'subtotal', 'shipping_cost', 'total', 
                  'shipping_address', 'shipping_city', 'shipping_state', 
                  'shipping_zip_code', 'shipping_phone', 'delivery_tracking_id',
                  'delivery_status', 'notes', 'items', 'created_at', 'updated_at')
        read_only_fields = ('order_number', 'status', 'payment_status', 'created_at', 'updated_at',
                           'delivery_tracking_id', 'delivery_status')


class CreateOrderSerializer(serializers.ModelSerializer):
    payment_method = serializers.ChoiceField(choices=['razorpay', 'cod'], default='cod')

    class Meta:
        model = Order
        fields = ('shipping_address', 'shipping_city', 'shipping_state', 
                  'shipping_zip_code', 'shipping_phone', 'payment_method', 'notes')

