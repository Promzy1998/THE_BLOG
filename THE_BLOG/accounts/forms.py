from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField( 
        widget=forms.TextInput(attrs={"placeholder": "Joe Clifford", "class": "form-input"})
    )
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "+17(23546783)", "class": "form-input"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "clifford1@gmail.com", "class": "form-input"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "clifford123k.com", "class": "form-input","id":"password"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "clifford123k.com", "class": "form-input","id":"confirmpassword"})
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone", "password1", "password2"]

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField( 
       widget=forms.TextInput(attrs={"placeholder": "Username", "class":"form-input","id":"username"})
    )
    password = forms.CharField(
       widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-input","id":"passLog"})
    )
