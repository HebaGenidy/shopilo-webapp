from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ContactMessage, Product, Category


class CustomUserCreationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)  

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'message']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image', 'stock']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']
