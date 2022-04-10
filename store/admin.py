from django.contrib import admin
from .models import Product,Category,User
from django.contrib.auth.admin import UserAdmin

admin.site.register(User,UserAdmin)



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['seller','name', 'price', 'quantity', 'available', 'created', 'updated']
    list_filter = ['seller','available', 'created', 'updated']
    list_editable = ['price', 'quantity', 'available']

admin.site.register(Product, ProductAdmin)