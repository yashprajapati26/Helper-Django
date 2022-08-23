from django.forms import ModelForm
from .models import User


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['email','first_name','mobileno','profession','state','city']

        
