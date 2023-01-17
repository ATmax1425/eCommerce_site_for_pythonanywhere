from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, ProductInCart, UserOrder


# def is_google_link(img_link):
#     print("is_google_link", img_link)
#     if "https://drive.google.com" not in str(img_link):
#         raise forms.ValidationError("Link should be from Google Drive")
#     elif not ("https://drive.google.com/file/d/" in img_link) and ("/view" in img_link):
#         raise forms.ValidationError("Link should be this form: 'https://drive.google.com/file/d/XXXXX/view'")


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password1"]


class ProductForm(forms.ModelForm):
    # img_url = forms.URLField(validators=[is_google_link])

    class Meta:
        model = Product
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['title'].widget.attrs = {'cols': 100}
    #     self.fields['description'].widget.attrs = {'cols': 120, 'rows': 5}


class OrderForm(forms.ModelForm):
    company_name = forms.CharField(required=False)

    class Meta:
        model = UserOrder
        fields = ['full_name', 'company_name', 'phone_num', 'Address_line1', 'Address_line2', 'pin_code',
                  'city', 'state']


class CartForm(forms.ModelForm):
    class Meta:
        model = ProductInCart
        fields = ["quantity"]
