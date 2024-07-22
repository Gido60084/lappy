from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(label='Username or Phone Number')
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
  
class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    debit_card_number = forms.CharField(max_length=16)
    expiration_date = forms.CharField(max_length=5)
    cvv = forms.CharField(max_length=3)  

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'location', 'profile_picture', 'phone_number', 'email_address']