from django.contrib import admin
from helper_app.models import Service,Service_category
# Register your models here.
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import format_html
from django.db import models
from django.urls import path
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from vendor_app.models import Book_Service

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



class ModelInlineService(admin.TabularInline):
    model = Service
    extra = 0

    fields = ("service_image","service_name","price","is_active","is_approved")
    formfield_overrides = {
            models.FileField: {'widget': AdminImageWidget}
        }
    # def service_image(self, obj):
    #     return format_html('<img src="{}" height=50px; width=70px />'.format(obj.service_image.url))

class ModelService_category(admin.ModelAdmin):
    inlines = [ModelInlineService,]
    list_display = [
            "category_name","Service_availbale"
        ]

        
    def Service_availbale(self,obj):
        return Service.objects.filter(category=obj).count()
    


admin.site.register(Service_category,ModelService_category)

class ServiceAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.FileField: {'widget': AdminImageWidget}
    }
    list_display = [
        "image","service_name","category","price","service_time","is_active","is_approved","action_button"
    ]


    def get_urls(self):
        urls = super(ServiceAdmin, self).get_urls()

        my_urls = [
            path('accept/<int:service_id>/', self.admin_site.admin_view(self.accept), name="accept"),
            path('reject/<int:service_id>/', self.admin_site.admin_view(self.reject), name="reject"),
        ]

        return my_urls + urls

    def accept(self, request, service_id):
        service = Service.objects.filter(id=service_id)
        service.update(is_approved = True)
        messages.success(request,f"Approved Service '{service.first().service_name}' ")
        #return HttpResponseRedirect(request.path_info)
        return redirect(request.META.get('HTTP_REFERER'))


    def reject(self, request, service_id):
        service = Service.objects.filter(id=service_id)
        service.update(is_approved = False)
        messages.success(request,f"Reject Service '{service.first().service_name}' ")
        #return HttpResponseRedirect(request.path_info) # for same url 
        return redirect(request.META.get('HTTP_REFERER'))




    def action_button(self, obj):
        if obj.is_approved:
            new_url = reverse("admin:reject", kwargs= {"service_id":obj.id})
            print(new_url)
            return format_html(u"""<p class='deletelink-box'><a href={0} class="deletelink">Reject</a></p>""", new_url)
        else:
            new_url = reverse("admin:accept", kwargs= {"service_id":obj.id})
            print(new_url)
            return format_html(u"""<p class=""><img src="/static/admin/img/icon-yes.svg" alt="True"><a href={0} class="acceptlink" style="color:green;"> Accept</a></p>""", new_url)

    action_button.short_description = 'Action'
    action_button.allow_tags = True

    def image(self, obj):
            return format_html('<img src="{}" height=50px; width=70px />'.format(obj.service_image.url))

    # image_tag.short_description = 'Image'

    

admin.site.register(Service,ServiceAdmin)


admin.site.register(Book_Service)