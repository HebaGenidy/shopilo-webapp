from django.urls import path
from django.contrib import admin
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
     path('all-products/', AllProductsView.as_view(), name='all_products'),
    path('category/<int:category_id>/', CategoryProductsView.as_view(), name='category_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='store/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='store/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='store/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='store/password_reset_complete.html'), name='password_reset_complete'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileView.as_view(), name='edit_profile'),
    path('category/<int:category_id>/', ProductByCategoryView.as_view(), name='all_product'),
    path('buy/<int:product_id>/', BuyProductView.as_view(), name='buy_product'),
    path('search/', ProductSearchView.as_view(), name='search_products'),
    path('cart/', CartView.as_view(), name='cart'),
    path('admin-panel/', AdminPanelView.as_view(), name='admin_panel'),
    path('admin-panel/products/add/', ProductCreateView.as_view(), name='product_add'),
    path('admin-panel/products/edit/<int:pk>/', ProductUpdateView.as_view(), name='product_edit'),
    path('admin-panel/products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('admin-panel/categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('admin-panel/categories/edit/<int:pk>/', CategoryUpdateView.as_view(), name='category_edit'),
    path('admin-panel/categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),


]
