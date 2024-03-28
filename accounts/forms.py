from django.core.exceptions import ValidationError
from django import forms
from .models import User
from phonenumber_field.formfields import PhoneNumberField
import phonenumbers, re


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["phone_number", "full_name"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number', 'full_name', 'is_admin', 'is_active']


class UserRegistrationForm(forms.Form):
    phone_number = PhoneNumberField(region='IR', label='شماره تلفن', widget=forms.TextInput(attrs={'class': 'sign_in_input', 'placeholder': 'شماره تلفن', 'id': 'id_phone_number', 'required': True}))
    full_name = forms.CharField(
        max_length=500, label='نام و نام خانوادگی',
        widget=forms.TextInput(
            attrs={'class': 'sign_in_input', 'placeholder': 'نام و نام خانوادگی', 'id': 'id_full_name',
                   'required': True})
    )

    password1 = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(
            attrs={'class': 'sign_in_input', 'placeholder': 'رمز عبور', 'id': 'id_password1', 'required': True})
    )

    password2 = forms.CharField(
        label='تایید رمز عبور',
        widget=forms.PasswordInput(
            attrs={'class': 'sign_in_input', 'placeholder': 'تایید رمز عبور', 'id': 'id_password2', 'required': True})
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords must match')
        return password2

    def clean_phone_number(self):

        phone_number = self.cleaned_data.get('phone_number')
        phone_number_str = str(phone_number)

        clean_number = re.sub(r'^(98|0)', '', phone_number_str)
        try:
            parsed_number = phonenumbers.parse(clean_number, "IR")
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
            return formatted_number
        except phonenumbers.phonenumberutil.NumberParseException:
            raise forms.ValidationError('شماره تلفن نامعتبر است')
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        full_name = cleaned_data.get('full_name')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if not phone_number:
            raise forms.ValidationError('این فیلد اجباری است')
        if not full_name:
            raise forms.ValidationError('این فیلد اجباری است')
        if not password1:
            raise forms.ValidationError('این فیلد اجباری است')
        if not password2:
            raise forms.ValidationError('این فیلد اجباری است')
        return cleaned_data


class UserLoginForm(forms.Form):
    phone_number = PhoneNumberField(region='IR', label='شماره تلفن', widget=forms.TextInput(attrs={'class': 'sign_in_input', 'placeholder': 'شماره تلفن', 'id': 'id_phone_number', 'required': True}))
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'class': 'sign_in_input', 'placeholder': 'رمز عبور', 'id': 'id_password1', 'required': True}))

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_number_str = str(phone_number)

        clean_number = re.sub(r'^(98|0)', '', phone_number_str)
        try:
            parsed_number = phonenumbers.parse(clean_number, "IR")
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
            return formatted_number
        except phonenumbers.phonenumberutil.NumberParseException:
            raise forms.ValidationError('شماره تلفن نامعتبر است')
        return phone_number


class UserEditProfileForm(forms.Form):
    phone_number = PhoneNumberField(region='IR', widget=forms.TextInput(
        attrs={'class': 'sign_in_input', 'placeholder': 'شماره تلفن', 'id': 'id_phone_number', 'required': True}))
    full_name = forms.CharField(max_length=500, widget=forms.TextInput(
        attrs={'class': 'sign_in_input', 'placeholder': 'نام و نام خانوادگی', 'id': 'id_full_name', 'required': True}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={'class': 'sign_in_input', 'placeholder': 'رمز عبور', 'id': 'id_password1', 'required': True}))
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(
        attrs={'class': 'sign_in_input', 'placeholder': 'تایید رمز عبور', 'id': 'id_password2', 'required': True}))


class UserOtpCodeForm(forms.Form):
    code = forms.IntegerField(label='کد')