from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import get_user_model

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name","password1", "password2")

class UserEditForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = [
            'first_name', 'last_name', 'bio',
            'dob','nickname','phone','ship_address','address2',
            'locality','state','postcode','country','bio']
        widgets = {
            'dob': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            )
        }


        