from django.contrib import admin
from .models import Category, Product, CustomUser, Address, Order,OrderItems

# Register your models here.

admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItems)

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display=['username', 'mobile_number', 'slug', 'pan', 'gstin', 'is_staff']
    list_filter=['username', 'mobile_number', 'pan', 'gstin']
    


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name', 'slug']
    prepopulated_fields={
        'slug':('name',)
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['name',  'slug', 'price', 'available', 'created', 'updated']
    list_filter=['name', 'created', 'updated']
    list_editable=['price', 'available']
    prepopulated_fields={
        'slug':('name',)
    }