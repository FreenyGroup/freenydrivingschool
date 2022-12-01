from django.forms import ModelForm, TextInput, EmailInput, NumberInput, DateInput
from .models import Order
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
User = get_user_model()
from django.forms import ModelForm, TextInput, EmailInput, NumberInput
from .models import Order
from django.contrib.auth import get_user_model
User = get_user_model()

class OrderCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address2'].required = False
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': "w-full rounded-lg border-gray-200 p-2.5 text-sm shadow-sm",
                'label': ''
            })
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 
        'ship_address','address2','locality', 'state', 'postcode',
        'country']
        widgets = {
            'ship_address': TextInput(attrs={
                'placeholder': '',
                'id': "ship_address",
                'name': "ship_address",
                'autocomplete': "off"
                }),
            'address2': TextInput(attrs={
                'placeholder': '',
                'id': "address2",
                'name': "address2",
                'autocomplete': "off",
                }),
            'postcode': NumberInput(attrs={
                'placeholder': '',
                'id': "postcode",
                'name': "postcode",
                'autocomplete': "off"
                }),
            'locality': TextInput(attrs={
                'placeholder': '',
                'id': "locality",
                'name': "locality",
                'autocomplete': "off"
                }) ,
            'state': TextInput(attrs={
                'placeholder': '',
                'id': "state",
                'name': "state",
                'autocomplete': "off"
                }),
            'country': TextInput(attrs={
                'placeholder': '',
                'id': "country",
                'name': "country",
                'autocomplete': "off",
                })
        }
