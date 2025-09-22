from django.db import models
from django.conf import settings
from orders.models import Order
User=settings.AUTH_USER_MODEL

class Payment(models.Model):
    STATUS_CHOICES=[
        ("initiated","Initiated"),
        ("success","Success"),
        ("failed","Failed"),
    ]
    order=models.OneToOneField(Order,related_name="payment",on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    authority=models.CharField(max_length=255,blank=True,null=True) #authority زرین پال
    ref_id=models.CharField(max_length=255,blank=True,null=True) #ref_id زرین پال 
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="initiated")
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"payment for Order{self.order_id}-{self.status}"
    