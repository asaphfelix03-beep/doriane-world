from django import forms


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(max_length=120, widget=forms.TextInput(attrs={"class": "form-control"}))
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )
