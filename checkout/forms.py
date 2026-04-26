from django import forms


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    address1 = forms.CharField(max_length=255)
    address2 = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)
    country = forms.CharField(max_length=100)
