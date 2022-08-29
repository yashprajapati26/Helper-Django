from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from helper_app.models import Service_category,Service
from django.views import View
from vendor_app.forms import ServiceForm
# Create your views here.


class HomeView(TemplateView):
    template_name = "Vendor/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_cats'] = Service_category.objects.all()[:]
        return context


class AddServiceView(View):
    def get(self,request):
        context = {}
        context['form'] = ServiceForm()
        return render(request,"Vendor/add_service.html",context)

    def post(self,request):
        context = {}
        service_form = ServiceForm(request.POST,request.FILES)

        if service_form.is_valid():
            obj = service_form.save(commit=False)
            obj.vendor = request.user
            obj.save()
            return HttpResponse("Add sucessfully")
        else:
            return HttpResponse("Something is wrong")

class MyServicesView(View):
    def get(self,request):
        context = {}
        context['services'] = Service.objects.filter(vendor=request.user)
        print(context['services'])
        return render(request,"Vendor/my_services.html",context)