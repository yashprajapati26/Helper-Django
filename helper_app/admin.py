from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from .models import User,OtpVerification,Vendor,Service,Service_category,Location
# Register your models here.
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib import messages
from django.contrib.admin import AdminSite
from .utils import send_mail_to_vendor
from django.utils.html import format_html
from django.db import models
from .models import Service

class AdminImageWidget(AdminFileWidget):

    def render(self, name, value, attrs=None, renderer=None):
        output = []

        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)

            output.append(
                f'<a href="{image_url}" target="_blank">'
                f'<img src="{image_url}" alt="{file_name}" width="80" height="80" '
                f'style="object-fit: cover;"/> </a>')

        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u''.join(output))



class UserAdmin(admin.ModelAdmin,AdminSite):
    list_display = [
         "email", "first_name", "user_type", "is_active",
    ]   
   

admin.site.register(User, UserAdmin)



class VendorAdmin(admin.ModelAdmin):
    list_display = [
        "email", "user_type", "is_active","is_vendor_approved"
    ]

    change_form_template = "Admin/add_btn.html"

    def get_urls(self):
        urls = super(VendorAdmin, self).get_urls()

        my_urls = [
            path('approved/<int:vendor_id>/', self.admin_site.admin_view(self.approved), name="approved"),
            path('rejected/<int:vendor_id>/', self.admin_site.admin_view(self.rejected), name="rejected"),
        ]

        return my_urls + urls

    def approved(self, request, vendor_id):

        obj = self.model.objects.get(id=vendor_id)
        obj.is_vendor_approved = True
        obj.save()
        email = obj.email
        msg = '''Hey Vendor!
                         I hope you doing well , this mail regarding to inform you that your request for vendor registration is confirm :) 
Now You can login with your email id and add service's.
                
Thank You. ''' 
        send_mail_to_vendor(email,msg)
        messages.success(request, "vendor '"+obj.email+"' has been approved")

        return HttpResponseRedirect("/admin/helper_app/vendor/")

    def rejected(self, request, vendor_id):
        obj = self.model.objects.get(id=vendor_id)
        obj.is_vendor_approved = False
        obj.save()
        email = obj.email
        msg = '''Hey Vendor!
                         I hope you doing well , this mail regarding to inform you that your request for vendor registration is Rejected becouse of some resoans  :(
                
Sorry For That. ''' 
        send_mail_to_vendor(email,msg)
        messages.error(request, "vendor '"+obj.email+"' has been rejected")

        return HttpResponseRedirect("/admin/helper_app/vendor/")

admin.site.register(Vendor,VendorAdmin)





class OtpVerificationAdmin(admin.ModelAdmin):
    list_display = [
        "user", "otp",
    ]   
 
admin.site.register(OtpVerification, OtpVerificationAdmin)





from django.db import models
from django.forms import Textarea
from django.contrib.postgres.fields import ArrayField

class LocationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ArrayField: {'widget': Textarea(attrs={'size':'90','rows':10, 'cols':40})},
    }


admin.site.register(Location,LocationAdmin)

