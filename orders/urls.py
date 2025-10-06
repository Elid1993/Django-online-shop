from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet ,OrderViewSet,view_cart

router=DefaultRouter()
router.register(r'cart',CartViewSet,basename='cart')
router.register(r'orders',OrderViewSet,basename='orders')

urlpatterns = [
    path('cart-view/',view_cart,name ='cart_view'),
]
urlpatterns += router.urls    

