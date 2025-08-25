from django.contrib import admin
from .models import Category, Product, Profile

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Profile)