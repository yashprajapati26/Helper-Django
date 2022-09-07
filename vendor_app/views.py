from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from helper_app.models import Service_category,Service
from django.views import View
from vendor_app.forms import ServiceForm
import datetime
from .forms import CheckoutForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

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
        return render(request,"Vendor/my_services.html",context)


class CheckoutView(LoginRequiredMixin,View):
    def get(self,request,pk):
        print("checkout")
        service = Service.objects.get(pk=pk)
        today = datetime.date.today()
        form = CheckoutForm()
        context = {'service':service,'today':today,'form':form}
        return render(request,"checkout.html",context)

    def post(self,request,pk):
        form = CheckoutForm(request.POST)
        service = Service.objects.get(pk=pk)
        if form.is_valid():
            data = form.save(commit=False)
            date = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time')
            data.datetime = datetime.datetime.combine(date, time)
            data.customer = request.user
            data.service = service
            data.save()
        else:
            messages.success(request,"something is wrong")
            return HttpResponseRedirect(request.path_info) # for same url 

        return HttpResponse("sucessfully added")




