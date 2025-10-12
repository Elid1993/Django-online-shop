from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name=models.CharField(max_length=150,unique=True)
    slug=models.SlugField(max_length=160,unique=True,blank=True)
    description=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name="Category"
        verbose_name_plural="Categories"
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug= slugify(self.name)
        super().save(*args,**kwargs)
    def __str__(self):
        return self.name
class Product(models.Model):
    category=models.ForeignKey(Category,related_name="products",on_delete=models.SET_NULL,null=True,blank=True)
    name=models.CharField(max_length=255)
    slug=models.SlugField(max_length=300,unique=True,blank=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField(default=0)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def save(self,*args,**kwargs):
        if not self.slug :
            base_slug=slugify(self.name)
            unique_slug=base_slug
            num=1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug=f"{base_slug}-{num}"
                num += 1
            self.slug=unique_slug
        super().save(*args,**kwargs) 
    
    def __str__(self):
        return self.name
    class Meta:
        ordering=["-created_at"]
     
class ProductImage(models.Model):
    product=models.ForeignKey(Product, related_name="images",on_delete=models.CASCADE)
    image=models.ImageField(upload_to="products/%y/%m/%d/")
    alt_text=models.CharField(max_length=255,blank=True)
    is_feature=models.BooleanField(default=False)
    def __str__(self):
        return f"Image for{self.product.name}"