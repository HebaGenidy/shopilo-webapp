from django.db import models
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# ------------ Category Model ------------

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', null=True, blank=True) 

    def __str__(self):
        return self.name

# ------------ Product Model ------------

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name

# ------------ Profile Model ------------

def user_profile_path(instance, filename):
    return f'profile_images/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(
        upload_to=user_profile_path,
        default='default/default.jpg',  
        blank=True
    )

    def __str__(self):
        return self.user.username

# ------------ Contact Message Model ------------

class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

# ------------ Edit Profile Model --------------

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'username']
    template_name = 'store/edit_profile.html'
    success_url = reverse_lazy('profile')  

    def get_object(self, queryset=None):
        return self.request.user


# ------------ cart model ---------------------

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity
