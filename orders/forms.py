from django import forms


class OrderPickupForm(forms.Form):
    pickup_datetime = forms.DateTimeField(
        label='Fecha y hora de recogida', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
