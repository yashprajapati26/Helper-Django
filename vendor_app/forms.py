from django import forms
from helper_app.models import Service,Service_category
from vendor_app.models import Book_Service

class ServiceForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Service_category.objects.all().order_by('category_name'),
        error_messages={'required': "Please select category"}
    )
    class Meta:
        model = Service
        fields = ["category","service_image","service_name","price","service_time","description","city"]
        
       
class CheckoutForm(forms.ModelForm):

    date = forms.DateField(           
    )

    time = forms.TimeField(
        error_messages={
            'required': "Please select time",
            'invalid': "Please select valid time"
        }
    )
    class Meta:
        model = Book_Service
        fields = ['fullname','address','city','state','pincode']
        