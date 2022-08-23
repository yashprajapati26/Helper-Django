from django import forms
from helper_app.models import Service,Service_category

class ServiceForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Service_category.objects.all().order_by('category_name'),
        error_messages={'required': "Please select category"}
    )
    class Meta:
        model = Service
        fields = ["category","service_image","service_name","price","service_time","description","city"]
        