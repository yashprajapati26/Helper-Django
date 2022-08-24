from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from helper_app.models import User,OtpVerification
import pyotp
from django.views.generic import TemplateView 
from .utils import send_otp_verification_mail
from .forms import RegisterForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from helper_app.models import *
from dyanamic_app.models import pages_content
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string

# Create your views here.

def index(request):
    all_cats = Service_category.objects.all()
    all_services = Service.objects.filter(is_approved=True,is_active=True)
    
    context = {'all_cats':all_cats,'all_services':all_services}
    context['how_we_do_it'] = pages_content.objects.get(name="how_we_do_it")
    context['what_we_are'] = pages_content.objects.get(name="what_we_are")

    return render(request,"index.html",context)

class LoginView(View):
    def get(self,request):
        return render(self.request,"login.html")
    
    def post(self,request):
        email = request.POST['email']
        print(email)
        user, created = User.objects.get_or_create(email=email)
        otp = pyotp.TOTP('base32secret3232') 
        otpobj, created = OtpVerification.objects.get_or_create(user=user)
        otpobj.otp = otp.now()
        print(otp.now())
        otpobj.save()
        send_otp_verification_mail(reciver=email,otp=otp.now())
        return render(self.request,"otp_verification.html",context={'email':email})

class OtpVerifyView(View):
    def post(self,request):
        user_otp = request.POST['otp']
        email=request.POST['email']
        user = User.objects.get(email=email)
        generate_otp = OtpVerification.objects.get(user=user).otp
        if generate_otp == user_otp:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(self.request, user)
            if user.user_type == "vendor" and user.is_vendor_approved == True:
                return redirect("vendor_app:home")
            return redirect("helper_app:index")
        else:
            msg = "OTP is Not match."
            return render(self.request,"otp_verification.html",context={'email':email,'msg':msg})
            

class RegisterView(View):
    def get(self,request):
        form = RegisterForm()
        return render(request,"register.html",{'RegisterForm':form})

    def post(self,request):
        form = RegisterForm(self.request.POST)
        
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.user_type = "vendor"
            form_obj.save()
            msg = "We will get into touch soon."
            return HttpResponse('''<center><div class="PartnerDetailsWidget__successMessage--2AcGg"><div class="LazyLoadImage__imageContainer--3EOU_ PartnerDetailsWidget__successIcon--C1ZIx"><div class="TemplateShimmer__shimmer--1HNwN TemplateShimmer__shimmerWrapper--Py2CJ TemplateShimmer__hidden--1oL9u"></div><img class="" src="https://s3-ap-southeast-1.amazonaws.com/urbanclap-prod/categories/category_v2/category_b24bd230.svg" alt="" itemscope="" itemprop="image"></div><span class="PartnerDetailsWidget__message--3NeRq">Thank you, we have received your details. Our team will get in touch with you soon.<a href="/">Go To Home Page</a></center>''')
        else:
            return redirect(request.META['HTTP_REFERER'])


class LogoutView(View):
    """
        Used to manage User Logout View
    """

    def get(self, *args, **kwargs):
        logout(self.request)
        messages.success(self.request, "Logged out successfully")
        return redirect("helper_app:login")



class ServicesView(TemplateView):
    template_name = "services.html"

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        page = 1
        services = Service.activate.all().order_by('-id')
        print(services)
        paginator = Paginator(services,3)
        next_url = ''
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            page = 2
            objects  = paginator.page(page)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        print(objects)
        context['all_services'] = objects.object_list
        context['all_cat'] = Service_category.objects.all()
        return context

@csrf_exempt
def load_more_service(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        print("called-------------")

        page = int(request.GET.get('page', 2))
        services = Service.activate.all().order_by('-id')
        print(services)
        paginator = Paginator(services,3)
        next_url = ''
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            page = 2
            objects  = paginator.page(page)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        print(objects)
        
        if objects.has_next():
            next_url = reverse("helper_app:load_more_service") + f"?page={int(page)+1}" 
            print(next_url)

            # http://localhost:8000/load_more_service/
            # ?page=3

        response = render_to_string("view_more_service.html",
                                    {"all_services": objects.object_list})


        return JsonResponse({
            'html': response,
            "status": "success",
            "next": next_url
        })









#----------------------------------------------------------------------------

from helper_app.models import Location
from django.http import JsonResponse

def maptime(request):

    return render(request,"Map/maptime.html")



@csrf_exempt
def final(request):
    import json

    total_data = json.loads(request.POST.getlist('myData[data]')[0])

    Location.objects.create(name ='test',data = total_data)

    # for i in total_data:
    #     Location.objects.create(name ='temp',data = i)
    #     print(i)

    return JsonResponse({'status':'success'})