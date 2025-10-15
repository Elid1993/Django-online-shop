from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import PaymentViewSet,payment_start,payment_verify,payment_success,payment_failed

# router =DefaultRouter()
# router.register("payment",PaymentViewSet,basename="payment")   

urlpatterns= [
    path("start/",payment_start, name="payment_start"),
    path("verify/",payment_verify,name="payment_verify"),
    path("success/",payment_success,name="payment_success"),
    path("failed/",payment_failed, name="payment_failed"),
]
