from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from django.views.decorators.csrf import  csrf_exempt
from django.utils.decorators import method_decorator
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer
from django.http import JsonResponse
from django.shortcuts import redirect,render

# 🟢 تابع کمکی برای گرفتن سبد خرید کاربر
def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

def view_cart(request):
    cart=get_cart(request)
    items=CartItem.objects.filter(cart=cart)
    total_amount=0
    cart_items=[]
    for item in items:
        total=item.product.price * item.quantity
        total_amount += total
        cart_items.append({
            "product":item.product,
            "quantity": item.quantity,
            "price":item.product.price,
            "total":total,
        })
        context ={
            "items": cart_items,
            "total_amount":total_amount,
        }
        return render(request,"cart.html", context)
 

@method_decorator(csrf_exempt, name='dispatch')
class CartViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @extend_schema(tags=["Orders"])
    def list(self, request):
        cart = get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        print("درخواست add_item دریافت شد", request.data)
        cart = get_cart(request)
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            item, created = CartItem.objects.get_or_create(
                cart=cart, product_id=product_id,
                defaults={'quantity': quantity}
            )
            if not created:
                item.quantity += quantity
                item.save()
            return Response(CartSerializer(cart).data)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        cart = get_cart(request)
        product_id = request.data.get('product_id')
        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()
            return Response(CartSerializer(cart).data)
        except CartItem.DoesNotExist:
            return Response({"detail": "item not found"}, status=404)

    @action(detail=False, methods=['post'])
    def clear_cart(self, request):
        cart = get_cart(request)
        cart.items.all().delete()
        return Response(CartSerializer(cart).data)


class OrderViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @extend_schema(tags=["Orders"])
    def list(self, request):
        if request.user.is_authenticated:
            orders = Order.objects.filter(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            orders = Order.objects.filter(session_key=request.session.session_key)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart = get_cart(request)
        if not cart.items.exists():
            return Response({"detail": "cart is empty"}, status=400)

        if request.user.is_authenticated:
            order = Order.objects.create(user=request.user, total_amount=cart.get_total_amount())
        else:
            order = Order.objects.create(session_key=request.session.session_key, total_amount=cart.get_total_amount())

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart.items.all().delete()

        return redirect(f"/api/payments/start/?order_id={order.id}")
        # return Response(OrderSerializer(order).data, status=201)



