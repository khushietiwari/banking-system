from django import forms
from django.contrib.auth.models import User
from corebank.models import Account


class CustomerForm(forms.ModelForm):  # For creating customer
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CustomerUpdateForm(forms.ModelForm):  # For updating
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['balance', 'status']
