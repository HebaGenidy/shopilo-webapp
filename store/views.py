from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .forms import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# ---------- Base Mixin for cart count & categories ----------
class BaseContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', [])
        context['cart_count'] = sum(item['quantity'] for item in cart)
        context['categories'] = Category.objects.all()
        return context


# ------------ Home View ---------------------------
class HomeView(BaseContextMixin, ListView):
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all().order_by('-id')[:12]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Reset cart_seen
        self.request.session['cart_seen'] = False
        self.request.session.modified = True
        return context


# ------------ Register View ------------------------
class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'store/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        return render(request, 'store/register.html', {'form': form})


# ------------ Product Detail View ----------------------
class ProductDetailView(BaseContextMixin, DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        product = self.object
        quantity = int(request.POST.get('quantity', 1))

        if quantity <= 0:
            messages.error(request, "Please enter a valid quantity.")
            return redirect('product_detail', pk=product.id)

        if quantity <= product.stock:
            product.stock -= quantity
            product.save()

            cart = request.session.get('cart', [])
            cart.append({
                'product_id': product.id,
                'name': product.name,
                'price': float(product.price),
                'quantity': quantity,
                'total': float(product.price) * quantity,
            })
            request.session['cart'] = cart
            request.session['cart_seen'] = False
            request.session.modified = True

            messages.success(request, f"Purchased {quantity} × {product.name} successfully.")
        else:
            messages.error(request, "The requested quantity is not available in stock.")

        return redirect('product_detail', pk=product.id)


# ------------ All Products View ------------------------
class AllProductsView(BaseContextMixin, ListView):
    model = Product
    template_name = 'store/all_product.html'
    context_object_name = 'products'
    ordering = ['-id']


# ------------ Category Products View ------------------------
class CategoryProductsView(BaseContextMixin, ListView):
    model = Product
    template_name = 'store/category.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


# ------------ Product By Category View -------------------------
class ProductByCategoryView(BaseContextMixin, ListView):
    model = Product
    template_name = 'store/all_product.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


# ------------ Login View ------------------------------
class LoginView(View):
    def get(self, request):
        return render(request, 'store/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # fixed lowercase
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'store/login.html')


# ------------ Contact View ------------------------------
class ContactView(View):
    def get(self, request):
        return render(request, 'store/home.html', {
            'products': Product.objects.all().order_by('-id'),
            'categories': Category.objects.all(),
            'success': False,
            'query': '',
        })

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"From: {first_name} {last_name}\nEmail: {email}\n\nMessage:\n{message}"

        send_mail(
            subject="New Contact Form Submission",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )

        return render(request, 'store/home.html', {
            'products': Product.objects.all().order_by('-id'),
            'categories': Category.objects.all(),
            'success': True,
            'query': '',
        })


# ------------ Profile View -----------------------
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        return render(request, 'store/profile.html')

    def post(self, request):
        profile = request.user.profile
        image = request.FILES.get('profile_image')
        if image:
            profile.profile_image = image
            profile.save()
        return redirect('profile')


# ------------ Buy Product View -------------------------
class BuyProductView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 0))

        if quantity <= 0:
            messages.error(request, "Please enter a valid quantity.")
            return redirect('product_detail', pk=product.id)

        if quantity <= product.stock:
            product.stock -= quantity
            product.save()

            cart = request.session.get('cart', [])
            cart.append({
                'product_id': product.id,
                'name': product.name,
                'price': float(product.price),
                'quantity': quantity,
                'total': float(product.price) * quantity,
            })
            request.session['cart'] = cart
            request.session['cart_seen'] = False
            request.session.modified = True

            messages.success(request, f"Purchase successful: {quantity} x {product.name}")
        else:
            messages.error(request, "Not enough stock available.")

        return redirect('product_detail', pk=product.id)


# ---------- Product Search View ----------------
class ProductSearchView(BaseContextMixin, ListView):
    model = Product
    template_name = 'store/search_results.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(name__icontains=query) if query else Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


# ------------ Cart View -------------------------------
class CartView(BaseContextMixin, TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', [])
        cart_items, total_price = [], 0

        for item in cart:
            product = get_object_or_404(Product, id=item['product_id'])
            quantity = item['quantity']
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })

        context['cart_items'] = cart_items
        context['total_price'] = total_price
        return context

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        if product_id:
            cart = request.session.get('cart', [])
            cart = [item for item in cart if str(item['product_id']) != str(product_id)]
            request.session['cart'] = cart
            request.session.modified = True
        return redirect('cart')


# ---------- Admin Required View ----------------
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


# ---------- Admin Panel & CRUD ----------------
class AdminPanelView(AdminRequiredMixin, BaseContextMixin, TemplateView):
    template_name = 'store/admin_panel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class ProductCreateView(AdminRequiredMixin, BaseContextMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('admin_panel')


class ProductUpdateView(AdminRequiredMixin, BaseContextMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('admin_panel')


class ProductDeleteView(AdminRequiredMixin, BaseContextMixin, DeleteView):
    model = Product
    template_name = 'store/product_confirm_delete.html'
    success_url = reverse_lazy('admin_panel')


class CategoryCreateView(AdminRequiredMixin, BaseContextMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'store/category_form.html'
    success_url = reverse_lazy('admin_panel')


class CategoryUpdateView(AdminRequiredMixin, BaseContextMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'store/category_form.html'
    success_url = reverse_lazy('admin_panel')


class CategoryDeleteView(AdminRequiredMixin, BaseContextMixin, DeleteView):
    model = Category
    template_name = 'store/category_confirm_delete.html'
    success_url = reverse_lazy('admin_panel')

