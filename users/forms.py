from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-transparent',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-transparent',
            'placeholder': 'Enter your last name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-transparent',
            'placeholder': 'Enter your email address'
        })
    )
    phone_number = forms.CharField(
        max_length=15, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-transparent',
            'placeholder': 'Enter your phone number'
        })
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add styling to remaining fields
        base_style = 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-transparent'
        
        self.fields['username'].widget.attrs.update({
            'class': base_style,
            'placeholder': 'Choose a username'
        })
        
        self.fields['password1'].widget.attrs.update({
            'class': base_style,
            'placeholder': 'Create a password'
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': base_style,
            'placeholder': 'Confirm your password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data["phone_number"]
            )
        return user
    
    
class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_style = 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-transparent'
        
        self.fields['username'].widget.attrs.update({
            'class': base_style,
            'placeholder': 'Enter your username'
        })
        
        self.fields['password'].widget.attrs.update({
            'class': base_style,
            'placeholder': 'Enter your password'
        })

    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500 accent-purple-600',
        })
    )

    class Meta:
        fields = ['username', 'password', 'remember_me']