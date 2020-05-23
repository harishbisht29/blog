from django import forms
from .models import Account, SubAccount

class SigninForm(forms.Form):
    email=  forms.EmailField( widget=forms.TextInput(
        attrs={'type':'email', 
        'placeholder': 'Enter email address'}
    ),label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password'}), label='')


class SignupForm(forms.ModelForm):
    email=  forms.EmailField( widget=forms.TextInput(
        attrs={'type':'email', 
        'placeholder': 'Enter email address'}
    ),label='')
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password'}), label='')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Re-Enter password'}), label='')
    username= forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    avatar = forms.ImageField(label='',required=False)

    class Meta:
        model= Account
        fields= ['email', 'username', 'password', 'confirm_password', 'avatar']
    
    def clean_confirm_password(self):
        password= self.cleaned_data.get("password")
        confirm_password= self.cleaned_data.get("confirm_password")
        if password and confirm_password and password!=confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password
    
    def save(self, commit=True):
        user= super().save(commit=False)
        user.set_password((self.cleaned_data["password"]))
        if commit:
            user.save()
        return user

class SubAccountForm(forms.ModelForm):
    email=  forms.EmailField( widget=forms.TextInput(
        attrs={'type':'email',
        'id':'email', 
        'placeholder': 'Type your email address'}
    ),label='')
    class Meta:
        model= SubAccount
        fields=['email',]