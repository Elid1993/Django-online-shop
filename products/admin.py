from django.contrib import admin
from .models import Category,Product,ProductImage
class ProductImageLine(admin.TabularInline):
    model=ProductImage
    extra=1
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":("name",)}
    list_display=("name","created_at")
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=("name","price","stock","is_active","created_at","slug")
    list_filter=("is_active","created_at")
    search_fields=("name","description")
    inlines=[ProductImageLine]
    prepopulated_fields={"slug":("name",)}
    