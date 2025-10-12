import requests
from django.shortcuts import render ,redirect
from django.conf import settings
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Payment
from drf_spectacular.utils import extend_schema
from .serializers import PaymentSerializer
from orders.models import Order

class PaymentViewSet(viewsets.ModelViewSet):
    queryset=Payment.objects.all()
    serializer_class=PaymentSerializer
    permission_classes=[IsAuthenticated]
    
    @extend_schema(
        tags=["Payments"]
    )
    @action(detail=False,methods=["post"],url_path="start")
    def start_payment(self,request):
        order_id=request.data.get("order_id")
        try:
            order =Order.objects.get(id=order_id,user=request.user)
        except Order .DoesNotExist:
            return Response({"detail":"Order not found "},status=404)
        # اگر پرداخت قبلی وجود داشت
        if hasattr(order,"payment"):
            payment=order.payment
        else:
            payment=Payment.objects.create(
                order=order,
                user=request.user,
                amount=order.total_amount
            )
        req_data={
            "merchant_id":settings.ZARINPAL_MERCHANT_ID,
            "amount":int(payment.amount),
            "callback_url":settings.CALLBACK_URL,
            "description":f"Payment for order {order.id}",
            "metadata":{"email":request.user.email}
        }
        res= requests.post(settings.ZARINPAL_REQUEST_URL,json=req_data)
        data=res.json()
        
        if "data" in data and data["data"].get("authority"):
            authority=data["data"]["authority"]
            payment.authority=authority
            payment.save()
            return Response({"payment_url":settings.ZARINPAL_STARTPAY_URL + authority})
        else:
            return Response (data,status=400)
    @action(detail=False,methods=["get"],url_path="verify")
    def verify_payment(self,request):
        authority= request.query_params.get("Authority")
        status_params= request.query_params.get("status")
        
        try:
            payment=Payment.objects.get(authority=authority)
        except Payment.DoesNotExist:  
            return render (request,"payment_failed.html")  
        if status_params != "OK":
            payment.status="failed"
            payment.save()
            return render(request,"payment_failed.html")
        req_data={
        "merchant_id":settings.ZARINPAL_MERCHANT_ID,
        "amount":int(payment.amount),
        "authority":authority   
        }
        
        res= requests.post(settings.ZARINPAL_VERIFY_URL,json=req_data)
        data =res.json()
        if "data" in data and data["data"].get("code")==100:
            payment.status="success"
            payment.ref_id=data["data"]["ref_id"]
            payment.save()
        # تغییر  وضعیت سفارش    
            order =payment.order
            order.status="paid"
            order.save()
            return render (request,"payment_success.html",{"ref_id":payment.ref_id,"amount":payment.amount })
        else:
            payment.status="failed"
            payment.save()
            return render (request,"payment_failed.html")

def payment_start(request):
    user=request.user if request.user.is_authenticated else None
    # (آخرین سفارش کاربر کخ پرداخت نشده)
    order=Order.objects.filter(user=user,status="pending").last()
    if not order:
        return render(request,"payment_failed.html",{"error": "سفارشی برای پرداخت وجود ندارد"})
    payment,created=Payment.objects.get_or_create(
        order=order,
        user=user,
        defaults={"amount":order.total_amount}
    )
    req_data={
        "merchant_id":settings.ZARINPAL_MERCHANT_ID,
        "amount":int(payment.amount),
        "callback_url":settings.CALLBACK_URL,
        "description":f"پرداخت سفترش شماره {order.id}",
        }
    res= requests.post(settings.ZARINPAL_REQUEST_URL,json=req_data)
    data=res.json()
        
    if "data" in data and data["data"].get("authority"):
        authority=data["data"]["authority"]
        payment.authority=authority
        payment.save()
        return redirect(settings.ZARINPAL_STARTPAY_URL + authority)
    else:
        return render(request,"payment_failed.html",{"error":"خطا در پرداخت با زرین پال"})

def payment_success(request):
    return render(request,"payment_success.html",{ "ref_id":"TEST12345","amount":150000,})
    
def payment_failed(request):
    return render (request,"payment_failed.html")
    
    