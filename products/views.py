from rest_framework import viewsets,permissions,filters
from .models import Category,Product,ProductImage
from drf_spectacular.utils import extend_schema,extend_schema_view
from .serializers import CategorySerializer,ProductSerializer,ProductImageSerializer
from rest_framework .permissions import IsAuthenticatedOrReadOnly,IsAdminUser
from .permissions import IsOwnerOrAdmin
from django.shortcuts import render,get_object_or_404

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["list","retrieve"]:
            return True
        return bool(request.user and request.user.is_staff)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    
    @extend_schema(
        tags=["Categories"]
    )    
    def get_permissions(self):
        if self .action in["create","update","partial_update","destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]
    
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    lookup_field="slug"  
    filter_backends=[filters.SearchFilter]  
    search_fields=["name","description"]
    
    @extend_schema(
        tags=["Products"]
    )
    def get_permissions(self):
        if self .action in["create","update","partial_update","destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]
    def get_queryset(self):
        qs=Product.objects.filter(is_active=True)
        category=self.request.query_params.get("category")
        min_price=self.request.query_params.get("min_price")
        max_price=self.request.query_params.get("max_price")
        if category:
            qs=qs.filter(category__slug=category)
        
        if min_price:
            try:
                qs=qs.filter(price__get=min_price)
            except ValueError:
                pass
        if max_price:
            try:
                qs=qs.filter(price__lte=max_price)
            except ValueError:
                pass 
        return qs
    
   
@extend_schema_view(
    tags=["ProductImages"]
    )

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset=ProductImage.objects.all()
    serializer_class=ProductImageSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]

def product_list(request):
    products=Product.objects.all().prefetch_related("images")
    return render (request, "product_list.html",{"products":products})

def product_detail(request,pk):
    product = get_object_or_404(Product.objects.prefetch_related("images"),pk=pk)
    return render(request,"product_detail.html",{"product":product})

def cart_view(request):
    return render (request,"cart.html")

def orders_view(request):
    return render (request,"orders.html")