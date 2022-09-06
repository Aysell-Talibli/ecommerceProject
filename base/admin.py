from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Profile, Product, Product_Companies, Category,Cart,Order,Order_product

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Product_Companies)
admin.site.register(Category)
admin.site.register(CustomUser)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Order_product)