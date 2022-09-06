from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . views import  Price, Cart_product, Order
urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('product/<int:pk>/give_price', Price.as_view(template_name="give_price.html"), name='price'),
    path('product/<int:pk>/', views.product_detail, name='detail'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('<str:username>/cart', Cart_product.as_view(), name='cart'),
    path('product/<int:pk>/order', Order.as_view(), name='order')
    
]
