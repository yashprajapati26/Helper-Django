from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
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
from django.db.models.query_utils import Q
from django.db.models import OuterRef
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import PasswordResetForm
from helper_app.decorators import user_is_vendor
# Create your views here.

@user_is_vendor
def index(request):
    # if request.user.user_type == "vendor":
    #     return redirect("vendor_app:home")

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



class password_reset_request(View):
    def get(self,request):
        password_reset_form = PasswordResetForm()
        return render(request, template_name="Admin/password_reset.html", context={"password_reset_form":password_reset_form})
        
    def post(self,request):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "Admin/password_reset_email.txt"
                    sender = settings.EMAIL_HOST_USER
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, sender , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")


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
from django.db.models import Count

class ServiceDetailsView(View):
    def get(self,request,service_id):
        context = {}
        service = Service.objects.get(pk=service_id)
        context['service'] = service
        context['related_service'] = Service.objects.filter(category=service.category)
        # context['category'] = Service_category.objects.all().annotate(counts = SubqueryCount(
        #     Service.objects.filter(category=OuterRef("pk")))).exclude(counts=0)
            #  ^
            # both same
            #  v
        context['category'] = Service_category.objects.annotate(counts = Count("service_cat")).exclude(counts=0)
        return render(request,"service_details.html",context)







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