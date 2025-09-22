from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart,CartItem,Order,OrderItem
from drf_spectacular.utils import extend_schema
from .serializers import CartSerializer,CartItemSerializer,OrderSerializer

class CartViewSet(viewsets.ViewSet):
    # queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=["Orders"]
    )
    def list(self, request):
        cart,_=Cart.objects.get_or_create(user=request.user)
        serializer=CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart,_=Cart.objects.get_or_create(user=request.user)
        serializer=CartItemSerializer(data=request.data)
        if serializer.is_valid():
            product_id=serializer.validated_data['product_id']
            quantity= serializer.validated_data['quantity']
            item,created=CartItem.objects.get_or_create(cart=cart,product_id=product_id,defaults={'quantity':quantity})
            if not created:
                item.quantity+=quantity
                item.save()
            return Response(CartSerializer(cart).data)
        return Response(serializer.errors,status=400)
    @action(detail=False,methods=['post'])
    def remove_item(self, request):
        cart,_=Cart.objects.get_or_create(user=request.user)
        product_id=request.data.get('product_id')
        try:
            item=CartItem.objects.get(cart=cart,product_id=product_id)
            item.delete()
            return Response(CartSerializer(cart).data)
        except CartItem.DoesNotExist:
            return Response({"detail":"item not found"},status=404)
    @action(detail=False,methods=['post'])
    def clear_cart(self, request):
        cart,_=Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response(CartSerializer(cart).data)
    
class OrderViewSet(viewsets.ViewSet):
    permission_classes=[IsAuthenticated]
    @extend_schema(
        tags=["Orders"]
    )
    def list(self, request):
        orders=Order.objects.filter(user=request.user)
        serializer=OrderSerializer(orders,many=True)
        return Response(serializer.data)
    @action(detail=False,methods=['post'])
    def checkout(self, request):
        cart,_=Cart.objects.get_or_create(user=request.user)
        if not cart.items.exists():
            return Response({"detail":"cart is empty"},status=400)
        order =Order.objects.create(user=request.user,total_amount=cart.get_total_amount())
        for item in cart.items.all():
            OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity,price=item.product.price)
        cart.items.all().delete()
        return Response(OrderSerializer(order).data,status=201)