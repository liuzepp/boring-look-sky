from django import forms
from Login.models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = UserAddressInfo
        fields = ['uname', 'uaddress', 'uphone']

        widgets = {
            'uaddress': forms.Textarea
        }
