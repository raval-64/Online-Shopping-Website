from django import forms
from django.contrib.auth.models import User
from .models import mobile_detail, address_info


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'log-form', 'placeholder': 'Username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'log-form', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'log-form', 'placeholder': 'Last Name'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'log-form', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'log-form', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'log-form', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        psw = cleaned_data.get("password")
        cpsw = cleaned_data.get("confirm_password")
        if psw != cpsw:
            self.add_error('confirm_password', 'Password and Confirm Password does not match')
        return self.cleaned_data


class MobileForm(forms.ModelForm):
    error = {'invalid': 'Enter a valid Mobile No'}
    mobile_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'log-form', 'placeholder': 'Mobile No'}), error_messages=error)

    class Meta:
        model = mobile_detail
        fields = ['mobile_no']


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
