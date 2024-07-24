from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, Category, Cart, CartItem, Order, OrderItem, UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .forms import LoginForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm, UserProfileForm


# Create your views here.


def homepage(request):
    products = Product.objects.all()
    return render(request, 'homepage.html', {'products': products})


def product_detail(request, product_id):
    products = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'products': products})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('homepage')


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def cart(request):
    products = Product.objects.all()
    return render(request, 'homepage.html', {'products': products})


def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = request.session.get("cart_id")

    if not cart_id:
        cart = Cart.objects.create()
        request.session["cart_id"] = cart.id
    else:
        cart = Cart.objects.get(id=cart_id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart_detail")


def checkout(request):
    cart = get_cart(request)
    total_amount = sum(item.product.price * item.quantity for item in cart.items.all())
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key,
                total_amount=total_amount
            )
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )
            cart.items.all().delete()  # Use related_name 'items'
            messages.success(request, 'Order placed successfully')
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()
    return render(request, 'checkout.html', {'form': form, 'cart': cart, 'total_amount': total_amount})


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})


def cart_detail(request):
    cart_id = request.session.get("cart_id")
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        cart_items = []

    return render(request, "cart_detail.html", {"cart_items": cart_items})


def search_products(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'search_results.html', {'products': products, 'query': query})


def about_view(request):
    return render(request, 'about.html')


def contact_page(request):
    return render(request, 'contact.html')


def services_page(request):
    return render(request, 'services.html')


def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page upon successful form submission
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile.html', {'form': form})


def edit_profile(request):
    user_profile = request.user.userprofile  # Assuming OneToOneField with User

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after successful update
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'form': form})
