from typing import Any
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Patient

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm):
        model = User
        fields = ("email", )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("The email is already taken.")
        return email
    
    def save(self, commit: bool = ...) -> Any:
        self.instance.username = self.instance.email
        return super().save(commit)

class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True)
    
    def save(self, commit: bool = ...) -> Any:
        self.instance.username = self.instance.email
        return super().save(commit)
    

class PatientCreationForm(CustomUserCreationForm):  
    first_name = forms.CharField(required=True)  
    class Meta:
        model = Patient
        fields = ("first_name", "phone", "gender", "email")

class CustomPatientChangeForm(CustomUserChangeForm):
    first_name = forms.CharField(required=True)  