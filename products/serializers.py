from rest_framework import serializers
from .models import Category,Product,ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=("id","product","image","alt_text","is_feature")
        
    def validate_image(self,value):
        max_size=5 *1024*1024
        if value.size>max_size:
            raise serializers.ValidationError("حجم نباید بیشتر از 5 مگابایت باشد")
        if not value.name.lower().endswith((".jpg",".jpeg",".png")):
            raise serializers.ValidationError("فقط jpg,png مجاز است ")
        return value 
class CategorySerializer(serializers.ModelSerializer):       
    class Meta:
        model=Category
        fields=("id","name","slug","description") 
        read_only_fields=["slug"] 
class ProductSerializer(serializers.ModelSerializer) :
    images=ProductImageSerializer(many=True, read_only=True)
    category=CategorySerializer(read_only=True)
    category_id=serializers.PrimaryKeyRelatedField(source="category",queryset=Category.objects.all(),write_only=True,required=False,allow_null=True)
    class Meta :
        model=Product
        fields=("id","name","slug","description","price","stock","is_active","category","category_id","images","created_at","updated_at")
        read_only_fields=("slug","created_at","updated_at")
    def create(self, validated_data):
        category=validated_data.pop("category",None)
        product=Product.objects.create(**validated_data)
        if category:
            product.category= category
            product.save()
        return product