from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet,ProductViewSet,ProductImageViewSet,product_list,product_detail,cart_view,orders_view


router= DefaultRouter()
router.register(r"categories",CategoryViewSet,basename="category")
router.register(r"products",ProductViewSet,basename="product")
router.register(r"product-images",ProductImageViewSet,basename="product_image")


urlpatterns =[
    path('api/',include (router.urls,)),
    path("",product_list,name ="product_list"),
    path("products/<int:pk>/",product_detail,name="product_detail"),
    path("cart/",cart_view,name="cart"),
    path("orders/",orders_view,name="orders_view"),
    ]