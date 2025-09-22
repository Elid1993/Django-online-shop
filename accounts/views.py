from rest_framework import generics ,permissions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema
from .serializers import RegisterSerializer, UserSerializer
User =get_user_model()

class RegisterAPIView(generics.CreateAPIView):
    queryset =User.objects.all()
    permissions_classes=[permissions.AllowAny]
    serializer_class=RegisterSerializer
    @extend_schema(
        tags=["Users"],
        request=RegisterSerializer,
        responses={201:UserSerializer},
        description="Register a new user.")
    
    def post (self,request,*args,**kwargs):
        return super().post(request,*args,**kwargs)
class CurrentUserAPIView(generics.RetrieveAPIView):
    permissions_classes =(permissions.IsAuthenticated)
    serializer_class=UserSerializer
    def get_object(self):
        return self.request.user
    @extend_schema(
        tags=["Users"],
        responses=UserSerializer,
        description="Get current logged-in user info."
    )
    
    def get(self,request,*args,**kwargs):
        return super().get(request,*args,**kwargs)
        
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
        def validate(self,attrs):
            data=super().validate(attrs)    
       #more information
            data.update({"username":self.user.username,"email":self.user.email,})
            return data
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer
    permissions_classes=[permissions.AllowAny]
    @extend_schema(
        tags=["Authentication"],
        request=MyTokenObtainPairSerializer,
        responses={200:MyTokenObtainPairSerializer},
        description="Obtain JWT token pair.")
    def post(self,request,*args,**kwargs):
        return super().post(request,*args,**kwargs)    
    
    