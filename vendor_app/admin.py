from django.contrib import admin
from helper_app.models import Service,Service_category
# Register your models here.
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import format_html
from django.db import models



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
        "image","service_name","category","price","service_time","is_active","is_approved"
    ]


    def image(self, obj):
            return format_html('<img src="{}" height=50px; width=70px />'.format(obj.service_image.url))

    # image_tag.short_description = 'Image'

admin.site.register(Service,ServiceAdmin)


