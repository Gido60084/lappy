from django.urls import path
from . import views
from .views import search_products, product_detail, about_view


urlpatterns = [
    path('', views.homepage, name = 'homepage'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('user_login/', views.user_login, name= 'user_login'),
    path('user_logout/', views.user_logout, name= 'user_logout'),
    path('signup/', views.signup, name= 'signup'),
    path('cart/', views.cart, name= 'cart'),
    path('search/', search_products, name='search_products'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('about/', about_view, name='about'),
    path('contact/', views.contact_page, name='contact_page'),
    path('services/', views.services_page, name='services_page'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]