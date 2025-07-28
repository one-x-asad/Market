from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Order, Product
from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm


class PhoneForm(forms.Form):
    phone = forms.CharField(
        max_length=9,
        label='📱 Telefon raqami (+998 bilan)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '901234567',
            'pattern': r'^\d{9}$',
            'title': 'Masalan: 901234567'
        })
    )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone.isdigit() or len(phone) != 9:
            raise forms.ValidationError("Faqat 9 ta raqam kiriting. Masalan: 901234567")
        return "+998" + phone  # To‘liq raqamni saqlaymiz


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Parolni kiriting",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol kiriting'})
    )
    password2 = forms.CharField(
        label="Parolni qayta kiriting",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni takrorlang'})
    )

    class Meta:
        model = User
        fields = ()  # Faqat parol, username esa session orqali qo‘yiladi

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Kiritilgan parollar mos emas!")
        return password2



class LoginForm(forms.Form):
    username = forms.CharField(label='Telefon raqam' )
    password = forms.CharField(widget=forms.PasswordInput)



class AddProduct(ModelForm):
    class Meta:
        model=Product
        fields="__all__"

class AddOrder(ModelForm):
    class Meta:
        model=Order
        fields="__all__"


