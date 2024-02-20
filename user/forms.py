from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telephone = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cell_phone = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name',
                  'last_name', 'address', 'location', 'telephone', 'cell_phone']
        
     

