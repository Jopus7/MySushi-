from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Order, Address, Payment


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = (
            'username',
            'email',
            'age',
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'age',
        )


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput,
    )


class OrderCreateForm(forms.ModelForm):
    delivery_address = forms.ModelChoiceField(
        queryset=Address.objects.none(),  # ustawimy dynamicznie w widoku
        label='Adres dostawy',
        required=True
    )
    payment_method = forms.ChoiceField(
        choices=Payment._meta.get_field('method').choices,
        label="Metoda płatności",
        required=True
    )
    class Meta:
        model = Order
        fields = ['delivery_address']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'zip_code', 'country']

