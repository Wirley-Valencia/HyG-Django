from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    location = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telephone = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cell_phone = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name',
                  'last_name', 'address', 'location', 'telephone', 'cell_phone']

    def clean(self):
        cleaned_data = super().clean()
        telephone = cleaned_data.get('telephone')
        cell_phone = cleaned_data.get('cell_phone')

        if telephone and len(telephone) < 10:
            self.add_error(
                'telephone', 'El teléfono debe tener al menos 10 dígitos.')

        if cell_phone and len(cell_phone) != 10:
            self.add_error('cell_phone', 'El celular debe tener 10 dígitos.')

        return cleaned_data
