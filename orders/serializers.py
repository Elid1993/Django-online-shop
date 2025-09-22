from rest_framework import serializers
from .models import Cart,CartItem,Order,OrderItem
from products.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total_price=serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "product_id","total_price"]
    def get_total_price(self, obj):
        return obj.get_total_price()
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)
    total_amount = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ["id", "items","total_amount"]
    def get_total_amount(self, obj):
        return obj.get_total_amount()

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price=serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ["id", "product","quantity","price","total_price"]
    def get_total_price(self, obj):
        return obj.get_total_price()

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only=True)
    total_amount = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id', 'items', 'status','total_amount','created_at']
    def get_total_amount(self, obj):
        return sum(item.get_total_price() for item in obj.items.all())