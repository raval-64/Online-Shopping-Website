from django import forms
from .models import address_info

class AddressForm(forms.ModelForm):
    error = {'invalid': 'Enter a valid Mobile No'}
    error1 = {'invalid': 'Enter a valid Pincode'}
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'add-form-field', 'placeholder': 'Name'}))
    mobile_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'add-form-field', 'placeholder': 'Mobile No'}), error_messages=error)
    pincode = forms.CharField(widget=forms.TextInput(attrs={'class': 'add-form-field', 'placeholder': 'Pincode','style': 'margin-bottom: 65px;'}), error_messages=error1)
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'add-form-field', 'placeholder': 'Address', 'rows': '5', 'cols': 'auto'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'add-form-field', 'placeholder': 'City'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'add-form-field', 'placeholder': 'State'}))

    class Meta:
        model = address_info
        fields = ['name', 'mobile_no', 'pincode', 'address', 'city', 'state']
